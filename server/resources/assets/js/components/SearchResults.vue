<template>
    <div>
        <div class="alert alert-success" v-if="amount > 0">
          Found {{ amount }} results for the query "{{ query }}"!
        </div>
        <div class="alert alert-warning" v-if="warning">
          {{ warning }}
        </div>

        <div class="well well-lg" v-for="doc in documents">
            
            <h3>
                <a :href="'/documents/' + doc.id">{{ doc.title }}</a>
            </h3>
            
            <span v-for="author in doc.authors">
                <span class="glyphicon glyphicon-user"></span>
                <a :href="'/authors/' + author.id"> {{ author.name }} </a>
            </span>
            
            <br><br>
            
            <p v-html="highlightQuery(doc.snippet)"></p>
            <small><a :href="'search?q=year:' + doc.year">Published in {{ doc.year }}</a></small><br />
            
            <strong>Tags:</strong>
            
            <a v-for="label in doc.labels" :href="'search?q=label:%22' + label.name + '%22'">
                <span class="tag label label-info">{{ label.name }}</span>
            </a>
            
        </div>

        <nav aria-label="Page navigation example">
          <ul class="pagination">
            <li class="page-item" @click="navigateTo(page-1)" :class="{disabled: page == 1}"><a class="page-link" href="#">Previous</a></li>
            <li class="page-item" @click="navigateTo(i)" :class="{active: page==i}" v-for="i in (1, Math.ceil(amount/10))"><a class="page-link" href="#">{{ i }}</a></li>
            <li class="page-item" @click="navigateTo(page+1)" :class="{disabled: page == Math.ceil(amount/10)}"><a class="page-link" href="#">Next</a></li>
          </ul>
        </nav>

    </div>
</template>

<script>
    export default {
        data: function(){
            return{
                documents: [],
                query: null,
                amount: 0,
                page: 1,
                warning: null
            }
        },
        mounted() {
            this.$parent.$on('query-results', data => this.handleResponse(data));
        },
        methods: {
            handleResponse(data) {
                if ('error' in data){
                    this.warning = data.error;
                }
                else{
                    this.documents = data.docs;
                    this.amount = data.amount;
                    this.query = data.query;
                }
            },
            highlightQuery(text){
                if (text != null && this.query != null){
                    var splitted_text = text.split(' ');
                    var queryWords = this.query.split(' ');
                    for (var i=0; i<splitted_text.length; i++){
                        if (queryWords.indexOf(splitted_text[i]) != -1){
                            splitted_text[i] = '<strong>' + splitted_text[i] + '</strong>';
                        }
                    }
                    return splitted_text.join(" ");
                }
                return "";
            },
            navigateTo(page) {
                this.page = page;
            }
        }
    }
</script>
