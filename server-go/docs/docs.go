// Package docs Code generated by swaggo/swag. DO NOT EDIT
package docs

import "github.com/swaggo/swag"

const docTemplate = `{
    "schemes": {{ marshal .Schemes }},
    "swagger": "2.0",
    "info": {
        "description": "{{escape .Description}}",
        "title": "{{.Title}}",
        "contact": {},
        "version": "{{.Version}}"
    },
    "host": "{{.Host}}",
    "basePath": "{{.BasePath}}",
    "paths": {
        "/bookmarks": {
            "get": {
                "description": "Returns all bookmarks",
                "produces": [
                    "application/json"
                ],
                "tags": [
                    "bookmarks"
                ],
                "summary": "Get list of bookmarks",
                "responses": {
                    "200": {
                        "description": "OK",
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/models.Bookmark"
                            }
                        }
                    },
                    "500": {
                        "description": "Internal Server Error",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    }
                }
            },
            "post": {
                "description": "Creates a new bookmark or updates an existing one",
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "tags": [
                    "bookmarks"
                ],
                "summary": "Create or update a bookmark",
                "parameters": [
                    {
                        "description": "Bookmark data",
                        "name": "bookmark",
                        "in": "body",
                        "required": true,
                        "schema": {
                            "$ref": "#/definitions/models.BookmarkCreateRequest"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Created",
                        "schema": {
                            "$ref": "#/definitions/models.Bookmark"
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    },
                    "500": {
                        "description": "Internal Server Error",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    }
                }
            }
        },
        "/chapters": {
            "post": {
                "description": "Creates a new chapter or updates the existing one if it already exists",
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "tags": [
                    "chapters"
                ],
                "summary": "Create or update a chapter",
                "parameters": [
                    {
                        "description": "Chapter to create or update",
                        "name": "chapter",
                        "in": "body",
                        "required": true,
                        "schema": {
                            "$ref": "#/definitions/models.Chapter"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Created",
                        "schema": {
                            "$ref": "#/definitions/models.Chapter"
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    },
                    "500": {
                        "description": "Internal Server Error",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    }
                }
            }
        },
        "/chapters/{ranobe_id}": {
            "get": {
                "description": "Returns all chapters for a specific ranobe",
                "produces": [
                    "application/json"
                ],
                "tags": [
                    "chapters"
                ],
                "summary": "Get list of chapters for a specific ranobe",
                "parameters": [
                    {
                        "type": "string",
                        "description": "Ranobe ID",
                        "name": "ranobe_id",
                        "in": "path",
                        "required": true
                    }
                ],
                "responses": {
                    "200": {
                        "description": "OK",
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/models.Chapter"
                            }
                        }
                    },
                    "404": {
                        "description": "Not Found",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    }
                }
            }
        },
        "/chapters/{ranobe_id}/{chapter_id}": {
            "get": {
                "description": "Fetch a chapter by ranobe_id and chapter_id",
                "produces": [
                    "application/json"
                ],
                "tags": [
                    "chapters"
                ],
                "summary": "Get a chapter",
                "parameters": [
                    {
                        "type": "string",
                        "description": "Ranobe ID",
                        "name": "ranobe_id",
                        "in": "path",
                        "required": true
                    },
                    {
                        "type": "string",
                        "description": "Chapter ID",
                        "name": "chapter_id",
                        "in": "path",
                        "required": true
                    }
                ],
                "responses": {
                    "200": {
                        "description": "OK",
                        "schema": {
                            "$ref": "#/definitions/models.Chapter"
                        }
                    },
                    "404": {
                        "description": "Not Found",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    }
                }
            }
        },
        "/chapters/{ranobe_id}/{chapter_id}/update_translation": {
            "put": {
                "description": "Update the Russian translation of a chapter",
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "tags": [
                    "chapters"
                ],
                "summary": "Update chapter translation",
                "parameters": [
                    {
                        "type": "string",
                        "description": "Ranobe ID",
                        "name": "ranobe_id",
                        "in": "path",
                        "required": true
                    },
                    {
                        "type": "string",
                        "description": "Chapter ID",
                        "name": "chapter_id",
                        "in": "path",
                        "required": true
                    },
                    {
                        "description": "Translation data",
                        "name": "translation",
                        "in": "body",
                        "required": true,
                        "schema": {
                            "$ref": "#/definitions/models.TranslationUpdate"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "OK",
                        "schema": {
                            "$ref": "#/definitions/models.Chapter"
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    },
                    "404": {
                        "description": "Not Found",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    }
                }
            }
        },
        "/ranobe": {
            "get": {
                "description": "Returns all ranobe with their titles, IDs, and associated chapters",
                "produces": [
                    "application/json"
                ],
                "tags": [
                    "ranobe"
                ],
                "summary": "Get ranobe list",
                "responses": {
                    "200": {
                        "description": "OK",
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/models.Ranobe"
                            }
                        }
                    },
                    "500": {
                        "description": "Internal Server Error",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    }
                }
            }
        },
        "/ranobe/create": {
            "post": {
                "description": "Creates a new ranobe with the given title",
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "tags": [
                    "ranobe"
                ],
                "summary": "Create a new ranobe",
                "parameters": [
                    {
                        "description": "Ranobe title to create",
                        "name": "ranobe",
                        "in": "body",
                        "required": true,
                        "schema": {
                            "$ref": "#/definitions/models.CreateRanobeRequest"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Created",
                        "schema": {
                            "$ref": "#/definitions/models.Ranobe"
                        }
                    },
                    "400": {
                        "description": "Bad Request",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    },
                    "500": {
                        "description": "Internal Server Error",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    }
                }
            }
        },
        "/ranobe/delete": {
            "delete": {
                "description": "Deletes the ranobe with the given ID",
                "tags": [
                    "ranobe"
                ],
                "summary": "Delete a ranobe",
                "parameters": [
                    {
                        "type": "string",
                        "description": "Ranobe ID",
                        "name": "id",
                        "in": "query",
                        "required": true
                    }
                ],
                "responses": {
                    "204": {
                        "description": "No Content"
                    },
                    "400": {
                        "description": "Bad Request",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    },
                    "500": {
                        "description": "Internal Server Error",
                        "schema": {
                            "$ref": "#/definitions/models.ErrorResponse"
                        }
                    }
                }
            }
        }
    },
    "definitions": {
        "models.Bookmark": {
            "type": "object",
            "properties": {
                "chapterID": {
                    "type": "integer"
                },
                "createdAt": {
                    "type": "string"
                },
                "id": {
                    "type": "string"
                },
                "ranobeID": {
                    "type": "string"
                },
                "updatedAt": {
                    "type": "string"
                }
            }
        },
        "models.BookmarkCreateRequest": {
            "type": "object",
            "required": [
                "chapter_id",
                "ranobe_id"
            ],
            "properties": {
                "chapter_id": {
                    "type": "integer"
                },
                "ranobe_id": {
                    "type": "string"
                }
            }
        },
        "models.Chapter": {
            "type": "object",
            "properties": {
                "chapter_id": {
                    "type": "integer"
                },
                "chapter_number_origin": {
                    "type": "integer"
                },
                "content_en": {
                    "type": "string"
                },
                "content_ru": {
                    "type": "string"
                },
                "id": {
                    "type": "string"
                },
                "ranobe_id": {
                    "type": "string"
                },
                "title_en": {
                    "type": "string"
                },
                "title_ru": {
                    "type": "string"
                }
            }
        },
        "models.CreateRanobeRequest": {
            "type": "object",
            "required": [
                "title"
            ],
            "properties": {
                "title": {
                    "type": "string"
                }
            }
        },
        "models.ErrorResponse": {
            "type": "object",
            "properties": {
                "error": {
                    "type": "string"
                }
            }
        },
        "models.Ranobe": {
            "type": "object",
            "properties": {
                "Chapters": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/models.Chapter"
                    }
                },
                "ID": {
                    "type": "string"
                },
                "Title": {
                    "type": "string"
                }
            }
        },
        "models.TranslationUpdate": {
            "type": "object",
            "properties": {
                "content_ru": {
                    "type": "string"
                },
                "title_ru": {
                    "type": "string"
                }
            }
        }
    }
}`

// SwaggerInfo holds exported Swagger Info so clients can modify it
var SwaggerInfo = &swag.Spec{
	Version:          "1.0",
	Host:             "localhost:8080",
	BasePath:         "/api",
	Schemes:          []string{},
	Title:            "Ranobe Reader API",
	Description:      "Это API для работы с ранобэ, главами и закладками",
	InfoInstanceName: "swagger",
	SwaggerTemplate:  docTemplate,
	LeftDelim:        "{{",
	RightDelim:       "}}",
}

func init() {
	swag.Register(SwaggerInfo.InstanceName(), SwaggerInfo)
}
