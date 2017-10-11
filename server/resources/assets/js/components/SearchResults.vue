<template>
    <div>
        <div class="well well-lg" v-for="doc in documents">
            <h3>{{ doc.title }}</h3>
            <span v-for="author in doc.authors">
                <span class="glyphicon glyphicon-user"></span>
                <a :href="'/authors/' + author.id"> {{ author.name }} </a>
            </span>
            <br><br>
            <p v-html="highlightQuery(doc.snippet)"></p>
            <small>Published in {{ doc.year }}</small><br />
            <strong>Tags:</strong>
            <a v-for="label in doc.labels" :href="'/labels/' + label.id">
                <span class="tag label label-info">
                    {{ label.name }} 
                </span>
            </a>
        </div>
    </div>
</template>

<script>
    export default {
        data: function(){
            return{
                documents: [],
                queryWords: []
            }
        },
        mounted() {
            this.$parent.$on('query-results', data => this.handleResponse(data));
        },
        methods: {
            handleResponse(data) {
                this.documents = data.docs;
                this.queryWords = data.query.split(" ");
            },
            highlightQuery(text){
                var splitted_text = text.split(' ');
                for (var i=0; i<splitted_text.length; i++){
                    if (this.queryWords.indexOf(splitted_text[i]) != -1){
                        splitted_text[i] = '<strong>' + splitted_text[i] + '</strong>';
                    }
                }
                return splitted_text.join(" ");
            }
        }
    }
</script>
