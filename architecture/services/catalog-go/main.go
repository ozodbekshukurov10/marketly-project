package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
)

type product struct {
	ID          int    `json:"id"`
	Title       string `json:"title"`
	Category    string `json:"category"`
	Price       string `json:"price"`
	Description string `json:"description"`
}

func main() {
	mux := http.NewServeMux()

	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, map[string]string{
			"service": "catalog-go",
			"status":  "ok",
		})
	})

	mux.HandleFunc("/api/v1/products", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, []product{
			{ID: 1, Title: "iPhone 15 Pro", Category: "Elektronika", Price: "12800000", Description: "Demo catalog response"},
			{ID: 2, Title: "iPhone 15 Pro Max", Category: "Elektronika", Price: "14500000", Description: "Demo catalog response"},
		})
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8081"
	}

	log.Printf("catalog-go listening on :%s", port)
	log.Fatal(http.ListenAndServe(":"+port, mux))
}

func writeJSON(w http.ResponseWriter, data any) {
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(data)
}
