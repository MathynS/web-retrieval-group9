
/**
 * First we will load all of this project's JavaScript dependencies which
 * includes Vue and other libraries. It is a great starting point when
 * building robust, powerful web applications using Vue and Laravel.
 */

require('./bootstrap');

window.Vue = require('vue');

/**
 * Next, we will create a fresh Vue application instance and attach it to
 * the page. Then, you may begin adding components to this application
 * or customize the JavaScript scaffolding to fit your unique needs.
 */

Vue.component('example', require('./components/Example.vue'));
Vue.component('searchbar', require('./components/SearchBar.vue'));
Vue.component('searchresults', require('./components/SearchResults.vue'));
Vue.component('author-field', require('./components/AuthorField.vue'));
Vue.component('author-graph', require('./components/AuthorGraph.vue'));
Vue.component('search-helper', require('./components/SearchHelper.vue'));

const app = new Vue({
    el: '#app'
});
