package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
)

type routeMap struct {
	Service string `json:"service"`
	Path    string `json:"path"`
	Method  string `json:"method"`
}

func main() {
	mux := http.NewServeMux()

	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, map[string]any{
			"service": "api-gateway-go",
			"status":  "ok",
		})
	})

	mux.HandleFunc("/routes", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, []routeMap{
			{Service: "identity-profile-java", Path: "/api/v1/auth/login", Method: "POST"},
			{Service: "identity-profile-java", Path: "/api/v1/profile", Method: "POST"},
			{Service: "catalog-go", Path: "/api/v1/products", Method: "GET"},
			{Service: "catalog-go", Path: "/api/v1/products", Method: "POST"},
			{Service: "compare-ai-cpp", Path: "/api/v1/compare/recommend", Method: "POST"},
		})
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("api-gateway-go listening on :%s", port)
	log.Fatal(http.ListenAndServe(":"+port, mux))
}

func writeJSON(w http.ResponseWriter, data any) {
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(data)
}
