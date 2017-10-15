<template>
    <div class="input-group">
        <input type="text" class="form-control" placeholder="Enter a search query" v-model="query">
        <span class="input-group-btn">p
            <button @click="submitQuery" class="btn btn-primary" type="button">Go!</button>
        </span>
    </div>
</template>

<script>
    export default {
        data: function(){
            return{
                query: null
            }
        },
        mounted() {
            this.query = this.getParameterByName('q');
            console.log(this.query);
            if (this.query != null){
                this.submitQuery();
            }
        },
        methods: {
            submitQuery(page) {
                page = typeof page !== 'undefined' ? page : 0;
                var pathname = window.location.pathname;
                if (pathname == '/search'){
                    axios.post('/api/search', {
                        query: this.query,
                        page: page
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
