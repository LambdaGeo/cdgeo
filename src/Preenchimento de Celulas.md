# Preenchimento de Celulas

- **Visão Geral**
    - **rasterstats**
        
        O rasterstats é um módulo em Python para sumarizar conjuntos de dados raster geoespaciais com base em geometrias vetoriais. Ele inclui funções para estatísticas zonais e consultas interpoladas de pontos. A interface de linha de comando permite fácil interoperabilidade com outras ferramentas GeoJSON.
        
    - **suporte a dados raster**
        
        O rasterstats possibilita trabalhar com qualquer fonte de dados raster suportada pelo [rasterio](https://github.com/rasterio/rasterio). Os dados podem ser categóricos (por exemplo, tipos de vegetação) ou valores contínuos (por exemplo, altitude).
        
    - **suporte a dados vetorias**
        
        O rasterstats oferece suporte flexível para elementos vetoriais com geometrias de Ponto, Linha, Polígono ou Multi*. Qualquer fonte de dados [fiona](https://fiona.readthedocs.io/en/stable/), GeoJSON, strings GeoJSON e formatos semelhantes, objetos que implementam [geo_interface](https://gist.github.com/sgillies/2217756) e representações de  geometrias WKT/WKB são todos suportados via submódulo **io**.
        
    - **início rápido**
        - Instalando
        
        ```bash
        pip install rasterstats
        ```
        
        - Calculando estatísticas descritivas de elevação, dada uma camada vetorial de polígonos (*polygons.shp*) e um modelo digital de elevação (DEM) rasterizado (*slope.tif*).
        
        ```python
        from rasterstats import zonal_stats
        zonal_stats("./polygons.shp", "./slope.tif", stats="count min mean max median")
        ```
        
        - O retorno é uma lista de dicionários. Cada dicionário dessa lista contém as estatísticas relacionadas ao “polígono” correspondente em *polygons.shp*.
        
        ```python
        [{'min': 6.575114727020264,
          'max': 22.273418426513672,
          'mean': 14.660084635416666,
          'count': 75,
          'median': 14.283852577209473},
         {'min': 16.940950393676758,
          'max': 82.69043731689453,
          'mean': 56.60576171875,
          'count': 50,
          'median': 55.908355712890625}]
        ```
        
    
- **Instalação**
    - **dependências**
        - libgdal
        - rasterio
        - fiona
        - shapely
        - numpy
        
    - **Ubuntu**
        - Para dependências como GDAL e numpy
        
        ```bash
        sudo apt-get install python-numpy libgdal1h gdal-bin libgdal-dev
        ```
        
        - Atualizando o pip (opcional)
        
        ```bash
        pip install --upgrade pip
        ```
        
        - Instalando rasterstats
        
        ```bash
        pip install rasterstats
        ```
        
    - **macOS**
        - Para a dependência GDAL
        
        ```bash
        brew install gdal
        ```
        
        - Atualizando o pip (opcional)
        
        ```bash
        pip install --upgrade pip
        ```
        
        - Instalando rasterstats
        
        ```bash
        pip install rasterstats
        ```
        
    - **Windows**
        - Atualizando o pip (opcional)
        
        ```bash
        python -m pip install --upgrade pip
        ```
        
        - Seguir a  [instalação do rasterio](https://github.com/rasterio/rasterio/blob/main/docs/installation.rst) e executar:
        
        ```bash
        pip install rasterstats
        ```
        
    
- **Manual do Usuário**
    - **Introdução**
        
        Dados geoespaciais geralmente se enquadram em um dos dois modelos de dados: 
        
        - **rasters:**  semelhantes a imagens com uma grade regular de pixels cujos valores representam algum fenômeno espacial (por exemplo, altitude);
        - **vetores:** entidades com geometrias discretas (por exemplo, limites de estados).
        
        O `rasterstats` existe exclusivamente para extrair informações de dados raster geoespaciais com base em geometrias vetoriais. Isso envolve, principalmente:
        
        - **estatísticas zonais:** método de resumir e agregar os valores raster que intersectam uma geometria vetorial. Por exemplo, estatísticas zonais fornecem respostas como a precipitação média ou a elevação máxima de uma unidade administrativa.
        - **consultas de pontos:** capacidade de consultar um raster em um ponto e obter um valor interpolado em vez do simples pixel mais próximo.
        
    - **Exemplo Básico**
        - O uso típico das funções do rasterstats envolve dois argumentos: **um** **vetor** e **um** **conjunto de dados** **raster**.
        
        ```python
        from rasterstats import zonal_stats, point_query
        stats = zonal_stats('./polygons.shp', './slope.tif')
        pts = point_query('./points.shp', './slope.tif')
        ```
        
        - **`zonal_stats`** retorna uma lista de dicionários. Cada dicionário contém as estatísticas relacionadas ao polígono de entrada correspondente no arquivo *polygons.shp*. Como *polygons.shp* contém apenas dois polígonos, a lista retornada conterá, igualmente, dois dicionários:
        
        ```python
        from pprint import pprint
        pprint(stats)
        ```
        
        ```python
        [{'count': 75,
          'max': 22.273418426513672,
          'mean': 14.660084635416666,
          'min': 6.575114727020264},
         {'count': 50,
          'max': 82.69043731689453,
          'mean': 56.60576171875,
          'min': 16.940950393676758}]
        ```
        
        - **`point_query`** retorna uma lista de valores raster correspondentes a cada ponto de entrada do arquivo *points.shp.* Como *points.shp* contém três pontos, a lista retornada contém, igualmente, 3 valores raster.
        
        ```python
        pts
        ```
        
        ```python
        [14.037668283186257, 33.1370268256543, 36.46848854950241]
        ```
        
    - **Fontes de Dados Vetoriais**
        - **Arquivos**
            - O caso de uso mais comum é ter fontes de dados vetoriais em um arquivo, como um ESRI Shapefile ou qualquer outro formato suportado pelo Fiona.
            
            - O caminho para o arquivo de dados vetoriais pode ser passado diretamente como o primeiro argumento, chamado `vectors` :
            
            ```python
            zs = zonal_stats('**./polygons.shp**', './slope.tif')
            ```
            
            - Se houver fontes de dados com **várias camadas**, é possível especificar a camada pelo nome ou índice, utilizando o parâmetro `layer`:
            
            ```python
            zs = zonal_stats('**./**', './slope.tif', layer="**polygons**")
            ```
            
        - **Lista de features GeoJSON ou semelhante**
            - O argumento `vectors`  também pode ser uma sequência de objetos que se comportam de forma semelhante aos objetos GeoJSON, os quais podem ser lidos diretamente de um arquivo usando Fiona:
            
            ```python
            import fiona
            with fiona.open('./polygons.shp') as src:
                zs = zonal_stats(src, 'slope.tif')
            ```
            
        - **Lista de objetos Python que suportam [geo_interface](https://gist.github.com/sgillies/2217756)**
            - O argumento `vectors` também pode ser uma sequência de objetos Python que implementam  __geo_interface__. Como exemplo, tem-se Shapely, ArcPy, PyShp, GeoDjango:
            
            ```python
            from shapely.geometry import Point
            pt = Point(245000, 1000000)
            pt.__geo_interface__
            ```
            
            ```python
            {'type': 'Point', 'coordinates': (245000.0, 1000000.0)}
            ```
            
            ```python
            point_query([pt.__geo_interface__], './slope.tif')
            ```
            
            ```python
            [21.32739672330894]
            ```
            
        - **Strings nos formatos de texto WKT e WKB**
            - em WKT:
            
            ```python
            pt.wkt
            ```
            
            ```python
            'POINT (245000 1000000)'
            ```
            
            ```python
            point_query([pt.wkt], './slope.tif')
            ```
            
            ```python
            [21.32739672330894]
            ```
            
            - em WKB:
            
            ```python
            pt.wkb
            ```
            
            ```python
            b'\x01\x01\x00\x00\x00\x00\x00\x00\x00@\xe8\rA\x00\x00\x00\x00\x80\x84.A'
            ```
            
            ```python
            point_query([pt.wkb], './slope.tif')
            ```
            
            ```python
            [21.32739672330894]
            ```
            
        
    - **Fontes de Dados Raster**
        - Qualquer formato que possa ser lido pelo `rasterio` é suportado pelo `rasterstats` .
        - **Testando fonte de dados**
            - Para testar se uma fonte de dados é suportada pela instalação (isso pode diferir dependendo do suporte de formato da biblioteca GDAL subjacente), tem-se a ferramenta de linha de comando rio:
            
            ```bash
            rio info raster.tif
            ```
            
        - **Arquivo**
            - O caminho para o arquivo raster pode ser especificado diretamente como segundo argumento da função:
            
            ```python
            zs = zonal_stats('./polygons.shp', '**./slope.tif**')
            ```
            
            - Se o raster contiver múltiplas bandas, é possível especificar a banda desejada (indexada partir de 1) por meio do parâmetro `band`:
            
            ```python
            zs = zonal_stats('./polygons.shp', './slope.tif', band=1)
            ```
            
        - **Numpy ndarray**
            - É possível passar um numpy `ndarray` como segundo argumento, em conjunto com uma transformação afim que mapeia as dimensões da matriz para um sistema de referência de coordenadas, utilizando o parâmetro `affine`:
            
            ```python
            import rasterio
            with rasterio.open('./slope.tif') as src:
            
                #Lendo os dados da primeira banda do raster
                array = src.read(1)   
            
                #Obtendo a transformação afim
                affine = src.transform  
                
                #Obtendo o valor nodata do raster
                nodata_value = src.nodata
                
            zs = zonal_stats('./polygons.shp', array, affine=affine, nodata=nodata_value)
            ```
            
        
    - **Estatísticas Zonais**
        - **Nativas**
            - **Padrões**
                
                Por padrão, a função `zonal_stats` retorna as seguintes estatísticas para os valores dos pixels contidos em cada zona (ou polígono) do dado vetorial:
                
                - **min** - valor mínimo
                - **max** - valor máximo
                - **mean** - média
                - **count**  - quantidade de pixels com valores válidos
                
            - **Opcionais**
                
                Opcionalmente, as seguintes estatísticas também estão disponíveis:
                
                - **sum** - soma
                - **std** - desvio padrão
                - **median** - mediana
                - **majoritary**  - moda
                - **minority** - valor menos comum (oposto da moda)
                - **unique** - quantidade de valores diferentes
                - **range** - diferença entre o valor máximo e o valor mínimo
                - **nodata** - quantidade de pixels marcados como ausentes
                - **percentile** - percentil
                
            - **Especificação**
                
                É possível especificar as estatísticas a serem calculadas de duas maneiras, ambas por meio do argumento `stats` :
                
                - **Como uma lista**:
                
                ```python
                stats = zonal_stats("./polygons.shp",
                                    "./slope.tif",
                                     stats=[**'min', 'max', 'median', 'majority', 'sum'**])
                ```
                
                - **Como uma string delimitada por espaços:**
                
                ```python
                stats = zonal_stats("./polygons.shp",
                                    "./slope.tif",
                                     stats=**'min max median majority sum'**)
                ```
                
            - **Observações**
                - Algumas estatísticas como majority, minority e unique exigem um processamento significativamente maior devido à contagem dispendiosa de ocorrências únicas para cada valor de pixel;
                
                - É possível utilizar a estatística de percentil especificando `percentile_<q>`, onde `<q>` pode ser um número decimal entre 0 e 100. Isso permite calcular o percentil desejado para os valores dos pixels, fornecendo mais flexibilidade na análise estatística dos dados.
                
            
        - **Personalizadas**
            - É possível definir funções agregadas usando o parâmetro `add_stats`. Ele recebe um dicionário com os nomes das estatísticas como chaves e as funções correspondentes como valores.
            
            - Por exemplo, para reimplementar a estatística de média
            
            ```python
            import numpy as np
            
            def minha_media(x):
                return np.ma.mean(x)
            
            zonal_stats("./polygons.shp", "./slope.tif",  
                         stats="count", add_stats={'minha_media':minha_media})
            
            ```
            
            ```python
            [{'count': 75, 'minha_media': 14.660084635416666},
             {'count': 50, 'minha_media': 56.60576171875}]
            ```
            
    

- Pequena ajuda com os passos
    
    texto jogado so para ver um passo que nao vi na documentacao
    
    Abrindo o dado vetorial:
    
    ```bash
    import geopandas as gpd
    gdf = gpd.read_file("data/brasil_grade_083_EPSG5880/brasil_grade_083_EPSG5880.shp")
    ```
    
    calculando as estaticas zonais, no caso so a media
    
    ```bash
    stats = zonal_stats ("data/brasil_grade_083_EPSG5880/brasil_grade_083_EPSG5880.shp", "data/brasil2010veg1.tif", stats="mean")
    ```
    
    adicionando ao geodataframe:
    
    ```bash
    gdf["mean_value"] = [feature["mean"] for feature in stats]
    ```
    
    plotando a estatistica calculada:
    
    ```bash
    gdf.plot(column='mean_value', cmap='viridis', legend=True, figsize=(10, 10))
    ```
    
    ![Untitled](Preenchimento%20de%20Celulas%20c7b509414c254f049cd159bf5d0f6da8/Untitled.png)
    
    salvando o dado vetorial com a informacao:
    
    ```bash
    gdf.to_file('saida.shp')
    ```
    

- Referências
    
    [https://slideplayer.com.br/slide/2712968/](https://slideplayer.com.br/slide/2712968/)
    
    [https://github.com/TerraME/terrame/wiki/Fill#Fill](https://github.com/TerraME/terrame/wiki/Fill#Fill)
    
    [http://mtc-m16b.sid.inpe.br/col/sid.inpe.br/MTC-m13@80/2006/08.10.18.21/doc/publicacao.pdf](http://mtc-m16b.sid.inpe.br/col/sid.inpe.br/MTC-m13@80/2006/08.10.18.21/doc/publicacao.pdf)