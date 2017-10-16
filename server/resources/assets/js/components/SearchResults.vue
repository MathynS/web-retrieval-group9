<template>
    <div>
        <div class="alert alert-success" v-if="amount >= 0">
          Found {{ amount }} results for the query "{{ query }}"!
        </div>
        <div class="alert alert-warning" v-if="warning">
          {{ warning }}
        </div>

        <span class="pull-right" v-if="documents.length > 0">
            <div class="dropdown">
                <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">{{ visualOrder }}
                    <span class="caret"></span>
                </button>

                <ul class="dropdown-menu">
                    <li><a @click="changeOrder('relevance')" href="#">Relevance</a></li>
                    <li><a @click="changeOrder('citations')" href="#">Citations</a></li>
                    <li><a @click="changeOrder('year_asc')" href="#">Date (old to new)</a></li>
                    <li><a @click="changeOrder('yearc_desc')" href="#">Date (new to old)</a></li>
                </ul>
            </div>
        </span>
        <br /><br />

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
            <small><a :href="'search?q=year:' + doc.year">Published in {{ doc.year }}</a></small>
            <span class="pull-right">Cited by {{ doc.citations }} papers</span>
            <br />

            <strong>Tags:</strong>
            
            <a v-for="label in doc.labels" :href="'search?q=label:%22' + label.name + '%22'">
                <span class="tag label label-info">{{ label.name }}</span>
            </a>
            
        </div>

        <nav aria-label="Page navigation example" v-if="documents.length > 0">
          <ul class="pagination">
            <li class="page-item" @click="navigateTo(page-1)" :class="{disabled: page == 1}"><a class="page-link" href="#">Previous</a></li>
            <li class="page-item" @click="navigateTo(i)" :class="{active: page==i}" v-for="i in (Math.max((5),1), Math.min(Math.max(10, (page+5)), Math.ceil(amount/10)))"><a class="page-link" href="#">{{ i }}</a></li>
            <li class="page-item" @click="navigateTo(page+1)" :class="{disabled: page == Math.ceil(amount/10)}"><a class="page-link" href="#">Next</a></li>
          </ul>
        </nav>

    </div>
</template>

<script>
    var sort_translate = {
        'relevance': 'Relevance',
        'citations': 'Citations',
        'year_asc': 'Date (old to new)',
        'year_desc': 'Date (new to old)'
    };

    export default {
        data: function(){
            return{
                sortOrder: 'Relevance',
                documents: [],
                query: null,
                amount: -1,
                page: 1,
                warning: null
            }
        },
        mounted() {
            this.$parent.$on('query-results', data => this.handleResponse(data));
        },
        methods: {
            changeOrder(sortOrder){
                window.location.replace('/search?q=' + this.query + '&page=' + this.page + '&order=' + sortOrder);
            },
            handleResponse(data) {
                if ('error' in data){
                    this.warning = data.error;
                }
                else{
                    this.documents = data.docs;
                    this.amount = data.amount;
                    this.query = data.query;
                    this.page = data.page;
                    this.visualOrder = sort_translate[data.order];
                    this.sortOrder = data.order;
                }
                console.log(this.page+5);
                console.log(Math.max((this.page-5),1), Math.min((this.page+5), Math.ceil(this.amount/10)));
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
                window.location.replace('/search?q=' + this.query + '&page=' + page + '&order=' + this.sortOrder);
            }
        }
    }
</script>
