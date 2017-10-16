<template>
    <div class="input-group">
        <input type="text" class="form-control" placeholder="Enter a search query" v-model="query">
        <span class="input-group-btn">p
            <button @click="manualSubmit()" class="btn btn-primary" type="button">Go!</button>
        </span>
    </div>
</template>

<script>
    export default {
        data: function(){
            return{
                query: null,
                page: 1,
                order: 'relevance'
            }
        },
        mounted() {
            this.query = this.getParameterByName('q');
            this.page = this.getParameterByName('page')
            this.order = this.getParameterByName('order');
            if (this.page == null){
                this.page = 1
            }
            if (this.order == null){
                this.order = 'relevance';
            }
            console.log(this.query, this.page, this.order);
            if (this.query != null){
                this.submitQuery();
            }
        },
        methods: {
            manualSubmit(){
                this.page = 1;
                this.order = 'relevance';
                this.submitQuery();
            },
            submitQuery() {
                var pathname = window.location.pathname;
                if (pathname == '/search'){
                    axios.post('/api/search', {
                        query: this.query,
                        page: this.page,
                        order: this.order
                    })
                    .then(response => this.$parent.$emit('query-results', response.data))
                    .catch(error => console.log(error));
                }
                else{
                    window.location.replace('/search?q=' + this.query);
                }
            },
            getParameterByName(name, url) {
                if (!url) url = window.location.href;
                name = name.replace(/[\[\]]/g, "\\$&");
                var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
                    results = regex.exec(url);
                if (!results) return null;
                if (!results[2]) return '';
                return decodeURIComponent(results[2].replace(/\+/g, " "));
            }
        }

    }
</script>
