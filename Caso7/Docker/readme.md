- Para lanzar la base de datos -> `docker-compose up`
- Para cargar los datos -> `python loadData.py`
  - Ten en cuenta que ni el script loadData.py ni la base de datos verifican la integridad de los datos.

- Puedes conectarte a MongoDB mediante MongoCompass usando la URL `mongodb://root:example@localhost:27017/ `
  - Esto es solo un ejemplo **NO DESPLEGAR EN PRODUCCIÓN**
  - La base de datos solo tiene el usuario _root_ y **la seguridad no está configurada**