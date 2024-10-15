package main

import (
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/swaggo/files"
	"github.com/swaggo/gin-swagger"
	_ "ranoberead-go/docs"
	"ranoberead-go/internal/handlers"
	"ranoberead-go/internal/models"
	"time"
)

// @title Ranobe Reader API
// @version 1.0
// @description Это API для работы с ранобэ, главами и закладками
// @host localhost:8080
// @BasePath /api
func main() {
	models.ConnectDB()

	r := gin.Default()

	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:5000"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Accept"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	// Swagger endpoint
	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	// Routes
	api := r.Group("/api")
	{
		// Ranobe routes
		api.GET("/ranobe", handlers.GetRanobeList)
		api.POST("/ranobe/create", handlers.CreateRanobe)
		api.DELETE("/ranobe/delete", handlers.DeleteRanobe)

		// Chapter routes
		api.GET("/chapters/:ranobe_id", handlers.GetChapterList)
		api.GET("/chapters/:ranobe_id/:chapter_id", handlers.GetChapter)
		api.POST("/chapters", handlers.CreateOrUpdateChapter)
		api.PUT("/chapters/:ranobe_id/:chapter_id/update_translation", handlers.UpdateChapterTranslation)

		// Bookmark routes
		api.GET("/bookmarks", handlers.ListBookmarks)
		api.POST("/bookmarks", handlers.CreateOrUpdateBookmark)
	}

	r.Run(":8080")
}
