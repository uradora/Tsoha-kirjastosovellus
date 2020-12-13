# Tsoha-kirjastosovellus

Kirjastosovellus

- [x] Sovellus pitää yllä listaa kirjoista, joilla on esim. genre, kirjailija ja yksi tai useampia arvosteluja.
- [x] Kirjoihin on hakutoiminto.
- [x] Käyttäjä voi lisätä mille tahansa kirjalle arvion (0-5 tähteä).
- [ ] Kirjoja voi ryhmitellä aakkosjärjestykseen genren, tekijän ja arvioiden mukaan.
- [x] Käyttäjätyypit ovat peruskäyttäjä ja ylläpitäjä.
- [x] Peruskäyttäjä voi lisätä arvosteluja, katsella kirjojen tietoja sekä tarkastella omaa lukulistaansa ja lisätä sinne kirjoja. 
- [x] Ylläpitäjä voi lisätä tai poistaa kirjoja kaikkien kirjojen luettelosta.

Heroku-linkki: https://tsoha-kirjastosovellus.herokuapp.com/

Sovelluksen etusivulla on lista kaikista kirjoista, jotka sovellukseen on lisätty sekä hakupalkki. Napsauttamalla kirjan nimestä pääsee tarkempiin tietoihin. Kirjautumaton käyttäjä voi tarkastella tietoja tästä linkistä, mutta vain kirjautunut käyttäjä voi lisätä arvioita tai lisätä kirjan omaan kirjalistaansa kirjan omasta näkymästä. Sisäänkirjautumiseen ja rekisteröitymiseen löytyvät painikkeet sovelluksen yläpalkin oikeasta yläkulmasta. Omaa kirjalistaa muokatakseen tai arvioita lisätäkseen pitää olla kirjautunut sisään. 

Lisäksi vain ylläpitäjä voi lisätä tai poistaa kirjoja. Kirjan voi lisätä etusivun linkistä ja sen voi poistaa seuraamalla kirjan nimestä napsauttamalla avautuvaa linkkiä. Näiden toiminnallisuuden herokussa testaamista varten käyttäjätunnus on admin ja salasana admin.

### Tunnettuja bugeja ja kehityssuunnitelmia

Sovellus kaatuu, kun yritetään lisätä kirjaa, jonka julkaisuvuosi-arvo on jotain muuta kuin numeerinen. Tämän voi korjata lisäämällä tulevaisuudessa input-validointia.
Kirjoille ei vielä saatu implementoitua tarkempaa hakua, jossa voidaan hakea esimerkiksi tekijän, genren tai julkaisuvuoden mukaan. Tämäkin on tarkoitus tehdä luomalla jonkinlainen lomake, jossa on input-validointia.
