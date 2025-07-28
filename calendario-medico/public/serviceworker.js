// nombre de la caché donde se guardarán los archivos de la app
const CACHE_NAME = `DentU-v1`;

// cuando se instala el service worker, se guarda en caché los archivos iniciales
self.addEventListener('install', event => {
  event.waitUntil((async () => {

    const cache = await caches.open(CACHE_NAME);

    // se agregan los archivos principales para que estén disponibles sin internet
    cache.addAll([
      '/registro.html',               // html
      '/registro.js',    
      '/registro.css'   
    ]);
  })());
});

// evento que intercepta las peticiones de la app o fetch
self.addEventListener('fetch', event => {
  event.respondWith((async () => {
    // se abre la caché
    const cache = await caches.open(CACHE_NAME);

    // busca respuesta en la caché
    const cachedResponse = await cache.match(event.request);
    if (cachedResponse) {
      // si el archivo está en la caché es devuelto
      return cachedResponse;
    } else {
      try {
        const fetchResponse = await fetch(event.request);

        cache.put(event.request, fetchResponse.clone());

        // se devuelve la respuesta original
        return fetchResponse;
      } catch (e) {
        // si no hay internet y el archivo no está en caché
        //  no se puede hacer nada
      }
    }
  })());
});
