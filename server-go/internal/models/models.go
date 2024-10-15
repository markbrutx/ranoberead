package models

import (
	"go.mongodb.org/mongo-driver/bson/primitive"
	"time"
)

type Ranobe struct {
	ID       primitive.ObjectID `bson:"_id,omitempty" json:"ID"`
	Title    string             `bson:"title" json:"Title"`
	Chapters []Chapter          `bson:"chapters,omitempty" json:"Chapters"`
}

type Chapter struct {
	ID                  primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	RanobeID            primitive.ObjectID `bson:"ranobe_id,omitempty" json:"ranobe_id"`
	ChapterID           int                `bson:"chapter_id" json:"chapter_id"`
	ChapterNumberOrigin int                `bson:"chapter_number_origin" json:"chapter_number_origin"`
	TitleRu             string             `bson:"title_ru" json:"title_ru"`
	TitleEn             string             `bson:"title_en" json:"title_en"`
	ContentRu           string             `bson:"content_ru" json:"content_ru"`
	ContentEn           string             `bson:"content_en" json:"content_en"`
}

type Bookmark struct {
	ID        primitive.ObjectID `bson:"_id,omitempty"`
	RanobeID  primitive.ObjectID `bson:"ranobe_id,omitempty"`
	ChapterID int                `bson:"chapter_id"`
	CreatedAt time.Time          `bson:"created_at"`
	UpdatedAt time.Time          `bson:"updated_at"`
}

// TranslationUpdate represents the translation data for updating a chapter
type TranslationUpdate struct {
	TitleRu   string `json:"title_ru"`
	ContentRu string `json:"content_ru"`
}
