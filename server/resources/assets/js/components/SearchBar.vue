<template>
    <div class="input-group">
        <input type="text" class="form-control" placeholder="Enter a search query" v-model="query">
        <span class="input-group-btn">
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
        methods: {
            submitQuery() {
                axios.post('/api/search', {
                    query: this.query
                })
                .then(response => this.$parent.$emit('query-results', response.data))
                .catch(error => console.log(error));
            }
        }

    }
</script>
