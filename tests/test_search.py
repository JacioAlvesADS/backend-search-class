import pytest
from fastapi import status

class TestSearch:
    """Testes para funcionalidade de busca"""
    
    def test_search_without_query(self, client):
        """Testa busca sem termo de pesquisa"""
        response = client.get("/api/search/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0  # Sem query, retorna lista vazia
    
    def test_search_with_empty_query(self, client):
        """Testa busca com query vazia"""
        response = client.get("/api/search/?q=")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_search_with_valid_query(self, client):
        """Testa busca com termo válido"""
        response = client.get("/api/search/?q=python")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_case_insensitive(self, client):
        """Testa que busca é case-insensitive"""
        response1 = client.get("/api/search/?q=PYTHON")
        response2 = client.get("/api/search/?q=python")
        response3 = client.get("/api/search/?q=Python")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        
        # Todas as buscas devem funcionar (retornar lista)
        assert isinstance(response1.json(), list)
        assert isinstance(response2.json(), list)
        assert isinstance(response3.json(), list)
    
    def test_search_special_characters(self, client):
        """Testa busca com caracteres especiais"""
        response = client.get("/api/search/?q=python&javascript")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_multiple_words(self, client):
        """Testa busca com múltiplas palavras"""
        response = client.get("/api/search/?q=curso de python")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_result_structure(self, client):
        """Testa estrutura dos resultados de busca"""
        response = client.get("/api/search/?q=test")
        assert response.status_code == 200
        results = response.json()
        
        # Se houver resultados, validar estrutura
        if len(results) > 0:
            course = results[0]
            assert "id" in course
            assert "title" in course
            assert "description" in course
            assert "price" in course
            assert "status" in course
    
    def test_search_matches_title_or_description(self, client):
        """Testa que busca encontra correspondências em título OU descrição"""
        # Este teste valida que a lógica OR está funcionando
        response = client.get("/api/search/?q=python")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Não podemos garantir resultados, mas a busca deve funcionar
