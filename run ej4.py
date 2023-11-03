from Ejercicio4 import leer_filtrar, heatmap_sim, pca_2d, pca_3d

title_no_filtrado, title_filtrado = leer_filtrar("salud", "archivo.csv")

heatmap_sim(title_no_filtrado, "Matriz de Similitud con stopwords")
heatmap_sim(title_filtrado, "Matriz de Similitud sin stopwords")

pca_2d(title_no_filtrado, 'Visualización de oraciones usando PCA con stopwords')
pca_2d(title_filtrado, 'Visualización de oraciones usando PCA sin stopwords')

pca_3d(title_no_filtrado, "Visualización en 3D con PCA s/stopwords")
pca_3d(title_filtrado, "Visualización en 3D con PCA c/stopwords")