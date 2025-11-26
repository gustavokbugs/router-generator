#include "grafo_db.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void inicializar_vertices(Grafo* g) {
    int i;
    char nome[20];
    
    // Inicializar esquinas (0-21)
    for (i = 0; i <= 21; i++) {
        sprintf(nome, "Esquina %d", i);
        adicionar_vertice(g, i, nome, "Esquina", "N/A", TIPO_ESQUINA);
    }

    // Pontos turísticos (22-119) - COM RUAS
    // R. 7 de Setembro
    adicionar_vertice(g, 22, "Pastelaria Pasteten Platz", "Restaurante", "R. 7 de Setembro", TIPO_PONTO);
    adicionar_vertice(g, 23, "BOTECO Spettu's Beer", "Bar", "R. 7 de Setembro", TIPO_PONTO);
    adicionar_vertice(g, 24, "AbraCachaça", "Bar", "R. 7 de Setembro", TIPO_PONTO);
    adicionar_vertice(g, 25, "Posto BR Mania Conveniência", "Posto de gasolina", "R. 7 de Setembro", TIPO_PONTO);
    adicionar_vertice(g, 26, "Di Capri", "Restaurante", "R. 7 de Setembro", TIPO_PONTO);

    // R. Borges de Medeiros
    adicionar_vertice(g, 27, "Barbudas", "Bar", "R. Borges de Medeiros", TIPO_PONTO);
    adicionar_vertice(g, 28, "Holy Sheep Craft Brewery", "Bar", "R. Borges de Medeiros", TIPO_PONTO);
    adicionar_vertice(g, 29, "Paragem Galeteria e Restaurante", "Restaurante", "R. Borges de Medeiros", TIPO_PONTO);
    adicionar_vertice(g, 30, "Parque Infantil", "Entretenimento", "R. Borges de Medeiros", TIPO_PONTO);
    adicionar_vertice(g, 31, "La Fiamma", "Restaurante", "R. Borges de Medeiros", TIPO_PONTO);
    adicionar_vertice(g, 32, "Melina Cozinha & Vinho", "Restaurante", "R. Borges de Medeiros", TIPO_PONTO);
    adicionar_vertice(g, 33, "Severo Garage", "Restaurante", "R. Borges de Medeiros", TIPO_PONTO);
    adicionar_vertice(g, 34, "Santa Poke", "Restaurante", "R. Borges de Medeiros", TIPO_PONTO);
    adicionar_vertice(g, 35, "Villa", "Restaurante", "R. Borges de Medeiros", TIPO_PONTO);
    adicionar_vertice(g, 36, "Heilige", "Cervejaria", "R. Borges de Medeiros", TIPO_PONTO);
    adicionar_vertice(g, 37, "Velasco", "Restaurante", "R. Borges de Medeiros", TIPO_PONTO);
    adicionar_vertice(g, 38, "Pizzaria Fornalha", "Restaurante", "R. Borges de Medeiros", TIPO_PONTO);

    // R. 28 de Setembro
    adicionar_vertice(g, 39, "Barbados", "Barbearia", "R. 28 de Setembro", TIPO_PONTO);
    adicionar_vertice(g, 40, "Sociedad", "Comércio", "R. 28 de Setembro", TIPO_PONTO);
    adicionar_vertice(g, 41, "Minhagriffe", "Comércio", "R. 28 de Setembro", TIPO_PONTO);
    adicionar_vertice(g, 42, "Dullius", "Moda e Vestuário", "R. 28 de Setembro", TIPO_PONTO);
    adicionar_vertice(g, 43, "Visual Modas", "Moda e Vestuário", "R. 28 de Setembro", TIPO_PONTO);
    adicionar_vertice(g, 44, "Armazém Kids", "Moda e Vestuário", "R. 28 de Setembro", TIPO_PONTO);
    adicionar_vertice(g, 45, "Pattussi", "Moda e Vestuário", "R. 28 de Setembro", TIPO_PONTO);
    adicionar_vertice(g, 46, "Dorinho", "Moda e Vestuário", "R. 28 de Setembro", TIPO_PONTO);
    adicionar_vertice(g, 47, "Clip Graffite 1", "Papelaria", "R. 28 de Setembro", TIPO_PONTO);
    adicionar_vertice(g, 48, "Colcci", "Moda e Vestuário", "R. 28 de Setembro", TIPO_PONTO);

    // Rua Júlio de Castilhos
    adicionar_vertice(g, 49, "Clip Graffite 2", "Papelaria", "R. Júlio de Castilhos", TIPO_PONTO);
    adicionar_vertice(g, 50, "Green Center", "Galeria", "R. Júlio de Castilhos", TIPO_PONTO);
    adicionar_vertice(g, 51, "Vanusa", "Moda e Vestuário", "R. Júlio de Castilhos", TIPO_PONTO);
    adicionar_vertice(g, 52, "Pioneira", "Moda e Vestuário", "R. Júlio de Castilhos", TIPO_PONTO);
    adicionar_vertice(g, 53, "Galeria Farah", "Galeria", "R. Júlio de Castilhos", TIPO_PONTO);
    adicionar_vertice(g, 54, "Le Chef", "Restaurante", "R. Júlio de Castilhos", TIPO_PONTO);
    adicionar_vertice(g, 55, "Praça Getúlio Vargas 1", "Centro Histórico", "R. Júlio de Castilhos", TIPO_PONTO);
    adicionar_vertice(g, 56, "Gang", "Moda e Vestuário", "R. Júlio de Castilhos", TIPO_PONTO);
    adicionar_vertice(g, 57, "Caixa", "Banco", "R. Júlio de Castilhos", TIPO_PONTO);
    adicionar_vertice(g, 58, "São João Farmácias 1", "Saúde", "R. Júlio de Castilhos", TIPO_PONTO);

    // Rua Ramiro Barcelos
    adicionar_vertice(g, 59, "Rodoil", "Posto de gasolina", "R. Ramiro Barcelos", TIPO_PONTO);
    adicionar_vertice(g, 60, "Coma Bem", "Restaurante", "R. Ramiro Barcelos", TIPO_PONTO);
    adicionar_vertice(g, 61, "Hotel Santa Cruz", "Hotel", "R. Ramiro Barcelos", TIPO_PONTO);
    adicionar_vertice(g, 62, "Sicredi", "Banco", "R. Ramiro Barcelos", TIPO_PONTO);
    adicionar_vertice(g, 63, "Bifão Grill", "Restaurante", "R. Ramiro Barcelos", TIPO_PONTO);
    adicionar_vertice(g, 64, "Santander", "Banco", "R. Ramiro Barcelos", TIPO_PONTO);
    adicionar_vertice(g, 65, "Catedral São João Batista", "Centro Histórico", "R. Ramiro Barcelos", TIPO_PONTO);
    adicionar_vertice(g, 66, "Praça Getúlio Vargas 2", "Centro Histórico", "R. Ramiro Barcelos", TIPO_PONTO);

    // Rua Venâncio Aires
    adicionar_vertice(g, 67, "Igreja Evangélica de Confissão Luterana", "Centro Histórico", "R. Venâncio Aires", TIPO_PONTO);
    adicionar_vertice(g, 68, "Panvel Farmácias", "Saúde", "R. Venâncio Aires", TIPO_PONTO);
    adicionar_vertice(g, 69, "Igreja Universal do Reino de Deus", "Centro Histórico", "R. Venâncio Aires", TIPO_PONTO);

    // Rua Tenente Coronel Brito
    adicionar_vertice(g, 70, "Praça da Bandeira", "Centro Histórico", "R. Tenente Coronel Brito", TIPO_PONTO);
    adicionar_vertice(g, 71, "Flamula Sports Bar", "Restaurante", "R. Tenente Coronel Brito", TIPO_PONTO);
    adicionar_vertice(g, 72, "Hotel Schulz", "Hotel", "R. Tenente Coronel Brito", TIPO_PONTO);
    adicionar_vertice(g, 73, "Churrascaria Centenário", "Restaurante", "R. Tenente Coronel Brito", TIPO_PONTO);
    adicionar_vertice(g, 74, "Brincasa", "Comércio", "R. Tenente Coronel Brito", TIPO_PONTO);
    adicionar_vertice(g, 75, "Nacional", "Supermercado", "R. Tenente Coronel Brito", TIPO_PONTO);
    adicionar_vertice(g, 76, "Kothe Esportes", "Moda e Vestuário", "R. Tenente Coronel Brito", TIPO_PONTO);
    adicionar_vertice(g, 77, "Panificadora Jamaica", "Padaria", "R. Tenente Coronel Brito", TIPO_PONTO);
    adicionar_vertice(g, 78, "São João Farmácias 2", "Saúde", "R. Tenente Coronel Brito", TIPO_PONTO);
    adicionar_vertice(g, 79, "Bradesco", "Banco", "R. Tenente Coronel Brito", TIPO_PONTO);
    adicionar_vertice(g, 80, "Lojas Becker", "Comércio", "R. Tenente Coronel Brito", TIPO_PONTO);

    // Rua Marechal Floriano
    adicionar_vertice(g, 81, "Charrua Hotel", "Hotel", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 82, "Dovino Adega", "Adega", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 83, "Central", "Bar", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 84, "Heilige Pocket", "Cervejaria", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 85, "Iluminura Livraria e Cafeteria", "Cafeteria", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 86, "HBier Public House", "Bar", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 87, "Hering", "Comércio", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 88, "Subway", "Restaurante", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 89, "Sorveteria da Mônica", "Doces", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 90, "Hbier Box", "Bar", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 91, "Renner", "Moda e Vestuário", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 92, "São João Farmácias 3", "Saúde", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 93, "Prata", "Moda e Vestuário", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 94, "oBoticario", "Comércio", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 95, "Ultramed Farmácias", "Saúde", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 96, "Casa do Papel", "Papelaria", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 97, "Rosa Norte", "Moda e Vestuário", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 98, "Magazine Luiza", "Comércio", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 99, "Casas Bahia", "Comércio", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 100, "Casa das Artes Regina Simonis", "Centro Histórico", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 101, "Quiosque", "Restaurante", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 102, "Monumento em homenagem às mães", "Centro Histórico", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 103, "Pompéia", "Moda e Vestuário", "R. Marechal Floriano", TIPO_PONTO);
    adicionar_vertice(g, 104, "Quero Quero", "Comércio", "R. Marechal Floriano", TIPO_PONTO);

    // Rua Marechal Deodoro
    adicionar_vertice(g, 105, "Minato Sushi", "Restaurante", "R. Marechal Deodoro", TIPO_PONTO);
    adicionar_vertice(g, 106, "OCTO Sushi", "Restaurante", "R. Marechal Deodoro", TIPO_PONTO);
    adicionar_vertice(g, 107, "Gatta di Latte Gelateria", "Doces", "R. Marechal Deodoro", TIPO_PONTO);
    adicionar_vertice(g, 108, "Nàpule Pizzeria", "Restaurante", "R. Marechal Deodoro", TIPO_PONTO);
    adicionar_vertice(g, 109, "Sr. Espetto Gastropub", "Restaurante", "R. Marechal Deodoro", TIPO_PONTO);
    adicionar_vertice(g, 110, "Kopenhagen", "Doces", "R. Marechal Deodoro", TIPO_PONTO);
    adicionar_vertice(g, 111, "Cheirin Bão", "Padaria", "R. Marechal Deodoro", TIPO_PONTO);
    adicionar_vertice(g, 112, "Flavia Eliel Calçados e Acessórios", "Moda e Vestuário", "R. Marechal Deodoro", TIPO_PONTO);
    adicionar_vertice(g, 113, "Dom Vito", "Moda e Vestuário", "R. Marechal Deodoro", TIPO_PONTO);
    adicionar_vertice(g, 114, "McDonald's", "Comércio", "R. Marechal Deodoro", TIPO_PONTO);
    adicionar_vertice(g, 115, "Banrisul", "Banco", "R. Marechal Deodoro", TIPO_PONTO);
    adicionar_vertice(g, 116, "Droga Raia Farmácias", "Saúde", "R. Marechal Deodoro", TIPO_PONTO);
    adicionar_vertice(g, 117, "Banco do Brasil", "Banco", "R. Marechal Deodoro", TIPO_PONTO);
    adicionar_vertice(g, 118, "Estacionamento e lavagem Bunker Car", "Estacionamento", "R. Marechal Deodoro", TIPO_PONTO);

    // Rua Venâncio Aires (A - U)
    adicionar_vertice(g, 119, "Praça Hardy Elmiro Martin", "Centro Histórico", "R. Venâncio Aires", TIPO_PONTO);
}

void inicializar_arestas(Grafo* g) {
    // LIGAÇÕES NA HORIZONTAL

    // R. 7 de Setembro (C → B)
    adicionar_aresta(g, 2, 24, 14);
    adicionar_aresta(g, 24, 23, 20);
    adicionar_aresta(g, 23, 22, 60);
    adicionar_aresta(g, 22, 1, 60);

    // R. 7 de Setembro (C ↔ D) - mão dupla
    adicionar_aresta(g, 2, 25, 14);
    adicionar_aresta(g, 25, 26, 90);
    adicionar_aresta(g, 26, 3, 50);
    // Sentido inverso
    adicionar_aresta(g, 3, 26, 50);
    adicionar_aresta(g, 26, 25, 90);
    adicionar_aresta(g, 25, 2, 14);

    // R. Borges de Medeiros (E → F)
    adicionar_aresta(g, 4, 27, 15);
    adicionar_aresta(g, 27, 28, 39);
    adicionar_aresta(g, 28, 5, 100);

    // R. Borges de Medeiros (F → G)
    adicionar_aresta(g, 5, 29, 34);
    adicionar_aresta(g, 29, 30, 6);
    adicionar_aresta(g, 30, 31, 14);
    adicionar_aresta(g, 31, 32, 40);
    adicionar_aresta(g, 32, 33, 30);
    adicionar_aresta(g, 33, 6, 30);

    // R. Borges de Medeiros (G → H)
    adicionar_aresta(g, 6, 34, 54);
    adicionar_aresta(g, 34, 35, 10);
    adicionar_aresta(g, 35, 36, 10);
    adicionar_aresta(g, 36, 37, 26);
    adicionar_aresta(g, 37, 38, 4);
    adicionar_aresta(g, 38, 7, 50);

    // R. 28 de Setembro (I → J)
    adicionar_aresta(g, 8, 39, 34);
    adicionar_aresta(g, 39, 40, 70);
    adicionar_aresta(g, 40, 9, 50);

    // R. 28 de Setembro (J → K)
    adicionar_aresta(g, 9, 41, 14);
    adicionar_aresta(g, 41, 42, 24);
    adicionar_aresta(g, 42, 43, 12);
    adicionar_aresta(g, 43, 44, 60);
    adicionar_aresta(g, 44, 10, 44);

    // R. 28 de Setembro (K → L)
    adicionar_aresta(g, 10, 45, 34);
    adicionar_aresta(g, 45, 46, 10);
    adicionar_aresta(g, 46, 47, 30);
    adicionar_aresta(g, 47, 48, 60);
    adicionar_aresta(g, 48, 11, 20);

    // Rua Júlio de Castilhos (M → N)
    adicionar_aresta(g, 12, 49, 44);
    adicionar_aresta(g, 49, 50, 66);
    adicionar_aresta(g, 50, 13, 44);

    // Rua Júlio de Castilhos (N → O)
    adicionar_aresta(g, 13, 51, 14);
    adicionar_aresta(g, 51, 52, 10);
    adicionar_aresta(g, 52, 53, 70);
    adicionar_aresta(g, 53, 14, 60);

    // Rua Júlio de Castilhos (O → P)
    adicionar_aresta(g, 14, 54, 70);
    adicionar_aresta(g, 54, 55, 4);
    adicionar_aresta(g, 55, 56, 6);
    adicionar_aresta(g, 56, 57, 34);
    adicionar_aresta(g, 57, 58, 26);
    adicionar_aresta(g, 58, 15, 14);

    // Rua Ramiro Barcelos (Q → R)
    adicionar_aresta(g, 16, 59, 84);
    adicionar_aresta(g, 59, 60, 30);
    adicionar_aresta(g, 60, 17, 40);

    // Rua Ramiro Barcelos (R → S)
    adicionar_aresta(g, 17, 61, 18);
    adicionar_aresta(g, 61, 62, 42);
    adicionar_aresta(g, 62, 63, 10);
    adicionar_aresta(g, 63, 18, 84);

    // Rua Ramiro Barcelos (S → T)
    adicionar_aresta(g, 18, 64, 18);
    adicionar_aresta(g, 64, 65, 46);
    adicionar_aresta(g, 65, 66, 10);
    adicionar_aresta(g, 66, 19, 80);

    // VERTICAIS

    // Rua Venâncio Aires (A → E)
    adicionar_aresta(g, 0, 67, 24);
    adicionar_aresta(g, 67, 4, 130);

    // Rua Venâncio Aires (E → I)
    adicionar_aresta(g, 4, 68, 140);
    adicionar_aresta(g, 68, 8, 14);

    // Rua Venâncio Aires (M → Q)
    adicionar_aresta(g, 12, 69, 100);
    adicionar_aresta(g, 69, 16, 54);

    // Rua Tenente Coronel Brito (B → F)
    adicionar_aresta(g, 1, 70, 74);
    adicionar_aresta(g, 70, 5, 80);

    // Rua Tenente Coronel Brito (F → J)
    adicionar_aresta(g, 5, 71, 10);
    adicionar_aresta(g, 71, 72, 34);
    adicionar_aresta(g, 72, 73, 6);
    adicionar_aresta(g, 73, 74, 54);
    adicionar_aresta(g, 74, 75, 10);
    adicionar_aresta(g, 75, 9, 40);

    // Rua Tenente Coronel Brito (J → N)
    adicionar_aresta(g, 9, 76, 40);
    adicionar_aresta(g, 76, 77, 65);
    adicionar_aresta(g, 77, 13, 49);

    // Rua Tenente Coronel Brito (N → R)
    adicionar_aresta(g, 13, 78, 24);
    adicionar_aresta(g, 78, 79, 70);
    adicionar_aresta(g, 79, 80, 36);
    adicionar_aresta(g, 80, 17, 24);

    // Rua Marechal Floriano (C → G)
    adicionar_aresta(g, 2, 81, 20);
    adicionar_aresta(g, 81, 82, 27);
    adicionar_aresta(g, 82, 83, 57);
    adicionar_aresta(g, 83, 84, 20);
    adicionar_aresta(g, 84, 85, 16);
    adicionar_aresta(g, 85, 6, 14);

    // Rua Marechal Floriano (G → K)
    adicionar_aresta(g, 6, 86, 12);
    adicionar_aresta(g, 86, 87, 2);
    adicionar_aresta(g, 87, 88, 10);
    adicionar_aresta(g, 88, 89, 6);
    adicionar_aresta(g, 89, 90, 30);
    adicionar_aresta(g, 90, 91, 26);
    adicionar_aresta(g, 91, 92, 54);
    adicionar_aresta(g, 92, 93, 2);
    adicionar_aresta(g, 93, 10, 12);

    // Rua Marechal Floriano (K → O)
    adicionar_aresta(g, 10, 94, 14);
    adicionar_aresta(g, 94, 95, 2);
    adicionar_aresta(g, 95, 96, 32);
    adicionar_aresta(g, 96, 97, 20);
    adicionar_aresta(g, 97, 98, 6);
    adicionar_aresta(g, 98, 99, 22);
    adicionar_aresta(g, 99, 100, 46);
    adicionar_aresta(g, 100, 14, 14);

    // Rua Marechal Floriano (O → S)
    adicionar_aresta(g, 14, 101, 36);
    adicionar_aresta(g, 101, 102, 50);
    adicionar_aresta(g, 102, 103, 30);
    adicionar_aresta(g, 103, 104, 24);
    adicionar_aresta(g, 104, 18, 14);

    // Rua Marechal Deodoro (D → H)
    adicionar_aresta(g, 3, 105, 14);
    adicionar_aresta(g, 105, 106, 30);
    adicionar_aresta(g, 106, 107, 28);
    adicionar_aresta(g, 107, 108, 24);
    adicionar_aresta(g, 108, 109, 44);
    adicionar_aresta(g, 109, 7, 14);

    // Rua Marechal Deodoro (H → L)
    adicionar_aresta(g, 7, 110, 104);
    adicionar_aresta(g, 110, 111, 36);
    adicionar_aresta(g, 111, 11, 14);

    // Rua Marechal Deodoro (L → P)
    adicionar_aresta(g, 11, 112, 14);
    adicionar_aresta(g, 112, 113, 18);
    adicionar_aresta(g, 113, 114, 48);
    adicionar_aresta(g, 114, 115, 2);
    adicionar_aresta(g, 115, 116, 58);
    adicionar_aresta(g, 116, 15, 14);

    // Rua Marechal Deodoro (P → T)
    adicionar_aresta(g, 15, 117, 62);
    adicionar_aresta(g, 117, 118, 26);
    adicionar_aresta(g, 118, 19, 66);

    // Rua Venâncio Aires (A → U)
    adicionar_aresta(g, 0, 119, 44);
    adicionar_aresta(g, 119, 20, 110);
}
