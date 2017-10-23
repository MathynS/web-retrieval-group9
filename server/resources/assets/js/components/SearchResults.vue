<template>
    <div>
        <div class="alert alert-success" v-if="amount >= 0">
          Found {{ amount }} results for the query `{{ query }}` in {{ responseTime }} seconds!
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
                    <li><a @click="changeOrder('year_desc')" href="#">Date (new to old)</a></li>
                </ul>
            </div>
        </span>
        <br /><br />

        <svg width="100%" :height="barHeight"></svg>

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
        'year_asc': 'Date (Oldest first)',
        'year_desc': 'Date (Newest first)'
    };

    export default {
        data: function(){
            return{
                sortOrder: 'Relevance',
                documents: [],
                query: null,
                amount: -1,
                page: 1,
                warning: null,
                barHeight: 0,
                responseTime: 0
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
                this.barHeight = 0;
                if ('error' in data){
                    this.warning = data.error;
                }
                else{
                    this.warning = null;    
                    this.documents = data.docs;
                    this.amount = data.amount;
                    this.query = data.query;
                    this.page = data.page;
                    this.visualOrder = sort_translate[data.order];
                    this.sortOrder = data.order;
                    this.responseTime = data.time;
                }
                if ('label_data' in data){
                    this.barHeight = 300;
                    this.drawChart(data.label_data);
                }
                console.log(this.page+5);
                console.log(Math.max((this.page-5),1), Math.min((this.page+5), Math.ceil(this.amount/10)));
            },
            highlightQuery(text){
                if (text != null && this.query != null){
                    var splitted_text = text.split(' ');
                    var queryWords = this.query.toLowerCase().split(' ');
                    for (var i=0; i<splitted_text.length; i++){
                        if (queryWords.indexOf(splitted_text[i].toLowerCase()) != -1){
                            splitted_text[i] = '<strong>' + splitted_text[i] + '</strong>';
                        }
                    }
                    return splitted_text.join(" ");
                }
                return "";
            },
            navigateTo(page) {
                window.location.replace('/search?q=' + this.query + '&page=' + page + '&order=' + this.sortOrder);
            },
            drawChart(data){
                var margin = {top: 20, right: 20, bottom: 70, left: 40},
                     width = 1000 - margin.left - margin.right,
                     height = 300 - margin.top - margin.bottom;

                // Parse the date / time
                var parseDate = d3.time.format("%Y").parse;

                var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

                var y = d3.scale.linear().range([height, 0]);

                var xAxis = d3.svg.axis()
                    .scale(x)
                    .orient("bottom")
                    .tickFormat(d3.time.format("%Y"));

                var yAxis = d3.svg.axis()
                    .scale(y)
                    .orient("left")
                    .ticks(10);

                var svg = d3.select("svg");

                    data.forEach(function(d) {
                        console.log(d);
                        d.date = parseDate(d.year.toString());
                        d.value = +d.count;
                    });
                    console.log(data);
                    
                  x.domain(data.map(function(d) { return d.date; }));
                  y.domain([0, d3.max(data, function(d) { return d.value; })]);

                  svg.append("g")
                      .attr("class", "x axis")
                      .attr("transform", "translate(0," + height + ")")
                      .call(xAxis)
                    .selectAll("text")
                      .style("text-anchor", "end")
                      .attr("dx", "-.8em")
                      .attr("dy", "-.55em")
                      .attr("transform", "rotate(-90)" );

                  svg.append("g")
                      .attr("class", "y axis")
                      .call(yAxis)
                    .append("text")
                      .attr("transform", "rotate(-90)")
                      .attr("y", 6)
                      .attr("dy", ".71em")
                      .style("text-anchor", "end")

                  svg.selectAll("bar")
                      .data(data)
                    .enter().append("rect")
                      .style("fill", "steelblue")
                      .attr("x", function(d) { return x(d.date); })
                      .attr("width", x.rangeBand())
                      .attr("y", function(d) { return y(d.value); })
                      .attr("height", function(d) { return height - y(d.value); });
                 
            }
        }
    }
</script>
