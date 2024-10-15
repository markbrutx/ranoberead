package handlers

import (
	"context"
	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo/options"
	"log"
	"net/http"
	"ranoberead-go/internal/models"
	"strconv"
)

// GetRanobeList godoc
// @Summary Get ranobe list
// @Description Returns all ranobe with their titles, IDs, and associated chapters
// @Tags ranobe
// @Produce json
// @Success 200 {array} models.Ranobe
// @Failure 500 {object} models.ErrorResponse
// @Router /ranobe [get]
func GetRanobeList(c *gin.Context) {
	collection := models.Client.Database("ranoberead").Collection("ranobe")
	chaptersCollection := models.Client.Database("ranoberead").Collection("chapters")

	cur, err := collection.Find(context.TODO(), bson.D{})
	if err != nil {
		log.Println("Error fetching ranobe:", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Server error"})
		return
	}
	defer cur.Close(context.TODO())

	var ranobes []models.Ranobe
	for cur.Next(context.TODO()) {
		var ranobe models.Ranobe
		err := cur.Decode(&ranobe)
		if err != nil {
			log.Println("Error decoding ranobe:", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Decoding error"})
			return
		}

		// Теперь запрашиваем главы для текущего ранобэ
		var chapters []models.Chapter
		filter := bson.M{"ranobe_id": ranobe.ID}
		curChapters, err := chaptersCollection.Find(context.TODO(), filter)
		if err != nil {
			log.Println("Error fetching chapters for ranobe:", ranobe.ID, err)
			continue
		}
		defer curChapters.Close(context.TODO())

		for curChapters.Next(context.TODO()) {
			var chapter models.Chapter
			err := curChapters.Decode(&chapter)
			if err != nil {
				log.Println("Error decoding chapter:", err)
				continue
			}
			chapters = append(chapters, chapter)
		}

		ranobe.Chapters = chapters // Добавляем главы в структуру ranobe
		ranobes = append(ranobes, ranobe)
	}

	c.JSON(http.StatusOK, ranobes)
}

// CreateRanobe godoc
// @Summary Create a new ranobe
// @Description Creates a new ranobe with the given title
// @Tags ranobe
// @Accept json
// @Produce json
// @Param ranobe body models.CreateRanobeRequest true "Ranobe title to create"
// @Success 201 {object} models.Ranobe
// @Failure 400 {object} models.ErrorResponse
// @Failure 500 {object} models.ErrorResponse
// @Router /ranobe/create [post]
func CreateRanobe(c *gin.Context) {
	var request models.CreateRanobeRequest
	if err := c.ShouldBindJSON(&request); err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{Error: "Invalid data"})
		return
	}

	ranobe := models.Ranobe{
		Title:    request.Title,
		Chapters: nil,
	}

	collection := models.Client.Database("ranoberead").Collection("ranobe")
	_, err := collection.InsertOne(context.TODO(), ranobe)
	if err != nil {
		log.Println("Error creating ranobe:", err)
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{Error: "Creation error"})
		return
	}

	c.JSON(http.StatusCreated, ranobe)
}

// DeleteRanobe godoc
// @Summary Delete a ranobe
// @Description Deletes the ranobe with the given ID
// @Tags ranobe
// @Param id query string true "Ranobe ID"
// @Success 204 "No Content"
// @Failure 400 {object} models.ErrorResponse
// @Failure 500 {object} models.ErrorResponse
// @Router /ranobe/delete [delete]
func DeleteRanobe(c *gin.Context) {
	ranobeID := c.Query("id")
	objID, err := primitive.ObjectIDFromHex(ranobeID)
	if err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{Error: "Invalid ID"})
		return
	}

	collection := models.Client.Database("ranoberead").Collection("ranobe")
	_, err = collection.DeleteOne(context.TODO(), bson.M{"_id": objID})
	if err != nil {
		log.Println("Error deleting ranobe:", err)
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{Error: "Deletion error"})
		return
	}

	c.JSON(http.StatusNoContent, nil)
}

// CreateOrUpdateChapter godoc
// @Summary Create or update a chapter
// @Description Creates a new chapter or updates the existing one if it already exists
// @Tags chapters
// @Accept json
// @Produce json
// @Param chapter body models.Chapter true "Chapter to create or update"
// @Success 201 {object} models.Chapter
// @Failure 400 {object} models.ErrorResponse
// @Failure 500 {object} models.ErrorResponse
// @Router /chapters [post]
func CreateOrUpdateChapter(c *gin.Context) {
	var chapter models.Chapter
	if err := c.ShouldBindJSON(&chapter); err != nil {
		log.Println("Invalid JSON data:", err)
		c.JSON(http.StatusBadRequest, models.ErrorResponse{Error: "Invalid data"})
		return
	}

	log.Printf("Received Chapter: %+v\n", chapter)

	if chapter.RanobeID.Hex() != "" {
		objRanobeID, err := primitive.ObjectIDFromHex(chapter.RanobeID.Hex())
		if err != nil {
			log.Println("Invalid Ranobe ID:", err)
			c.JSON(http.StatusBadRequest, models.ErrorResponse{Error: "Invalid Ranobe ID"})
			return
		}
		chapter.RanobeID = objRanobeID
	}

	collection := models.Client.Database("ranoberead").Collection("chapters")

	// Check if chapter already exists
	filter := bson.M{"ranobe_id": chapter.RanobeID, "chapter_id": chapter.ChapterID}
	update := bson.M{"$set": chapter}
	opts := options.Update().SetUpsert(true)

	_, err := collection.UpdateOne(context.TODO(), filter, update, opts)
	if err != nil {
		log.Println("Error creating or updating chapter:", err)
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{Error: "Creation or update error"})
		return
	}

	c.JSON(http.StatusCreated, chapter)
}

// GetChapter godoc
// @Summary Get a chapter
// @Description Fetch a chapter by ranobe_id and chapter_id
// @Tags chapters
// @Produce json
// @Param ranobe_id path string true "Ranobe ID"
// @Param chapter_id path string true "Chapter ID"
// @Success 200 {object} models.Chapter
// @Failure 404 {object} models.ErrorResponse
// @Router /chapters/{ranobe_id}/{chapter_id} [get]
func GetChapter(c *gin.Context) {
	ranobeID := c.Param("ranobe_id")
	chapterID := c.Param("chapter_id")

	objRanobeID, err := primitive.ObjectIDFromHex(ranobeID)
	if err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{Error: "Invalid Ranobe ID"})
		return
	}

	objChapterID, err := strconv.Atoi(chapterID)
	if err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{Error: "Invalid Chapter ID"})
		return
	}

	collection := models.Client.Database("ranoberead").Collection("chapters")
	filter := bson.M{"ranobe_id": objRanobeID, "chapter_id": objChapterID}

	var chapter models.Chapter
	err = collection.FindOne(context.TODO(), filter).Decode(&chapter)
	if err != nil {
		c.JSON(http.StatusNotFound, models.ErrorResponse{Error: "Chapter not found"})
		return
	}

	c.JSON(http.StatusOK, chapter)
}

// UpdateChapterTranslation godoc
// @Summary Update chapter translation
// @Description Update the Russian translation of a chapter
// @Tags chapters
// @Accept json
// @Produce json
// @Param ranobe_id path string true "Ranobe ID"
// @Param chapter_id path string true "Chapter ID"
// @Param translation body models.TranslationUpdate true "Translation data"
// @Success 200 {object} models.Chapter
// @Failure 400 {object} models.ErrorResponse
// @Failure 404 {object} models.ErrorResponse
// @Router /chapters/{ranobe_id}/{chapter_id}/update_translation [put]
func UpdateChapterTranslation(c *gin.Context) {
	ranobeID := c.Param("ranobe_id")
	chapterID := c.Param("chapter_id")

	objRanobeID, err := primitive.ObjectIDFromHex(ranobeID)
	if err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{Error: "Invalid Ranobe ID"})
		return
	}

	objChapterID, err := strconv.Atoi(chapterID)
	if err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{Error: "Invalid Chapter ID"})
		return
	}

	var translation models.TranslationUpdate
	if err := c.ShouldBindJSON(&translation); err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{Error: "Invalid data"})
		return
	}

	collection := models.Client.Database("ranoberead").Collection("chapters")
	filter := bson.M{"ranobe_id": objRanobeID, "chapter_id": objChapterID}
	update := bson.M{
		"$set": bson.M{
			"title_ru":   translation.TitleRu,
			"content_ru": translation.ContentRu,
		},
	}

	_, err = collection.UpdateOne(context.TODO(), filter, update)
	if err != nil {
		c.JSON(http.StatusNotFound, models.ErrorResponse{Error: "Chapter not found"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Translation updated successfully"})
}

// GetChapterList godoc
// @Summary Get list of chapters for a specific ranobe
// @Description Returns all chapters for a specific ranobe
// @Tags chapters
// @Produce json
// @Param ranobe_id path string true "Ranobe ID"
// @Success 200 {array} models.Chapter
// @Failure 404 {object} models.ErrorResponse
// @Router /chapters/{ranobe_id} [get]
func GetChapterList(c *gin.Context) {
	ranobeID := c.Param("ranobe_id")

	objRanobeID, err := primitive.ObjectIDFromHex(ranobeID)
	if err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{Error: "Invalid Ranobe ID"})
		return
	}

	collection := models.Client.Database("ranoberead").Collection("chapters")
	filter := bson.M{"ranobe_id": objRanobeID}

	cur, err := collection.Find(context.TODO(), filter)
	if err != nil {
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{Error: "Error fetching chapters"})
		return
	}
	defer cur.Close(context.TODO())

	var chapters []models.Chapter
	for cur.Next(context.TODO()) {
		var chapter models.Chapter
		err := cur.Decode(&chapter)
		if err != nil {
			c.JSON(http.StatusInternalServerError, models.ErrorResponse{Error: "Decoding error"})
			return
		}
		chapters = append(chapters, chapter)
	}

	if len(chapters) == 0 {
		c.JSON(http.StatusNotFound, models.ErrorResponse{Error: "No chapters found"})
		return
	}

	c.JSON(http.StatusOK, chapters)
}

// ListBookmarks godoc
// @Summary Get list of bookmarks
// @Description Returns all bookmarks
// @Tags bookmarks
// @Produce json
// @Success 200 {array} models.Bookmark
// @Failure 500 {object} models.ErrorResponse
// @Router /bookmarks [get]
func ListBookmarks(c *gin.Context) {
	collection := models.Client.Database("ranoberead").Collection("bookmarks")

	cur, err := collection.Find(context.TODO(), bson.D{})
	if err != nil {
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{Error: "Error fetching bookmarks"})
		return
	}
	defer cur.Close(context.TODO())

	var bookmarks []models.Bookmark
	for cur.Next(context.TODO()) {
		var bookmark models.Bookmark
		err := cur.Decode(&bookmark)
		if err != nil {
			c.JSON(http.StatusInternalServerError, models.ErrorResponse{Error: "Decoding error"})
			return
		}
		bookmarks = append(bookmarks, bookmark)
	}

	c.JSON(http.StatusOK, bookmarks)
}

// CreateOrUpdateBookmark godoc
// @Summary Create or update a bookmark
// @Description Creates a new bookmark or updates an existing one
// @Tags bookmarks
// @Accept json
// @Produce json
// @Param bookmark body models.BookmarkCreateRequest true "Bookmark data"
// @Success 201 {object} models.Bookmark
// @Failure 400 {object} models.ErrorResponse
// @Failure 500 {object} models.ErrorResponse
// @Router /bookmarks [post]
func CreateOrUpdateBookmark(c *gin.Context) {
	var request models.BookmarkCreateRequest
	if err := c.ShouldBindJSON(&request); err != nil {
		c.JSON(http.StatusBadRequest, models.ErrorResponse{Error: "Invalid data"})
		return
	}

	collection := models.Client.Database("ranoberead").Collection("bookmarks")

	// Check if bookmark already exists
	filter := bson.M{"ranobe_id": request.RanobeID}
	update := bson.M{"$set": bson.M{"chapter_id": request.ChapterID}}
	opts := options.Update().SetUpsert(true)

	_, err := collection.UpdateOne(context.TODO(), filter, update, opts)
	if err != nil {
		c.JSON(http.StatusInternalServerError, models.ErrorResponse{Error: "Error creating or updating bookmark"})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"message": "Bookmark created or updated"})
}
