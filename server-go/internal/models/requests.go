package models

import "go.mongodb.org/mongo-driver/bson/primitive"

// CreateRanobeRequest is the request for creating a new Ranobe
type CreateRanobeRequest struct {
	Title string `json:"title" binding:"required"`
}

// BookmarkCreateRequest represents the request for creating or updating a bookmark
type BookmarkCreateRequest struct {
	RanobeID  primitive.ObjectID `json:"ranobe_id" binding:"required"`
	ChapterID int                `json:"chapter_id" binding:"required"`
}
