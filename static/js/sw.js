const cacheName = 'ARCODERS-v2';
const staticAssets = [
    '/static/js/manifest.json',
    '/static/js/pwa.js',
    '/static/js/rating.js',
    '/static/CSS/navigation.css',
    '/static/CSS/slidebar.css',
    '/static/CSS/scroll.css',
    '/static/CSS/screen_size.css',
    '/static/CSS/arbuttons and more.css',
    '/static/CSS/footer.css',
    '/static/CSS/base.css',
    '/static/CSS/nav.css',
    '/static/js/base.js',
    '/static/js/nav.js',
    '/static/js/slidebar.js',
    '/static/CSS/home.css',
    '',
    '/static/images/logo/test.png'

];





self.addEventListener('install', async e => {
    const cache = await caches.open(cacheName);
    await cache.addAll(staticAssets);
    return self.skipWaiting();
})




self.addEventListener('activate', e => {
    self.clients.claim();

})

self.addEventListener('fetch', async e => {
    const req = e.request;
    const url = new URL(req.url);
    
    if (url.origin === location.origin) {
        e.respondWith(cacheFirst(req));
    } else {
        e.respondWith(networkAndCache(req));
    }
});


async function cacheFirst(req) {
    const cache = await caches.open(cacheName);
    const cached = await cache.match(req);
    return cached || fetch(req);
}


async function networkAndCache(req) {
    const cache = await caches.open(cacheName);
    try{
        const fresh = await fetch(req);
        await cache.put(req, fresh.clone());
        return fresh;
    } catch(e) {
        const cached = await cache.match(req);
        return cached;
    }
}



// self.addEventListener('install', function (event) {
    //     event.waitUntil(
        //         caches.open(cacheName).then(function (cache) {
            //             return cache.addAll([
                //                 staticAssets
//             ]);
//         })
//     );
// });




// addEventListener('install', event => {
//     const preCache = async () => {
//         const cache = await caches.open(cacheName);
//         return cache.addAll([
//             // staticAssets
//             '/static/js/manifest.json',
//             '/static/js/pwa.js',
//             '/static/js/rating.js',
//             '/static/CSS/navigation.css',
//             '/static/CSS/slidebar.css',
//             '/static/CSS/scroll.css',
//             '/static/CSS/screen_size.css',
//             '/static/CSS/arbuttons and more.css',
//             '/static/CSS/footer.css',
//             '/static/CSS/base.css',
//             '/static/CSS/nav.css',
//             '/static/js/base.js',
//             '/static/js/nav.js',
//             '/static/js/slidebar.js',
//             '/static/CSS/home.css',
//             '',
//             '/static/images/logo/test.png'

//         ]);
//     };
//     event.waitUntil(preCache());
// });
