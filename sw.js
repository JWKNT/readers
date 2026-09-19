/* Retirement endpoint for existing v1-v3 registrations. Not registered by v4. */
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',event=>event.waitUntil((async()=>{const prefix='readers-offline:'+self.registration.scope+':';for(const k of await caches.keys())if(k.startsWith(prefix))await caches.delete(k);await self.registration.unregister();})()));
