<template>
    <div class="container">
        <h3>Query Builder</h3>

        <p>
        With the query builder you can easily build advanced queries by using the input below<br>
        Fill in one or multiple boxes to search on. <br>
        If you want multiple value to match for a specific filter click on the button OR to specify the different possible matches
        </p>

        <p>{{query}}</p>

        <div class="row">
            <div class="col-lg-8">
                <form>
                    <div class="form-group" v-for="(value, key) in filters">

                        <div class="input-group">
                            <span class="input-group-addon" id="query_label">{{key}}</span>
                            <input type="text" v-model="value['queries'][0]" class="form-control" aria-describedby="query_label">
                            <span class="input-group-btn">
                                <button class="btn btn-secondary" type="button" @click="filters[key]['amount'] += 1">OR</button>
                            </span>
                        </div>
                        <br>
                        <div class="form-group row" v-for="n in value['amount']">
                            <label :for="'label' + key + n" class="col-sm-1 col-form-label">OR</label>
                            <div class="col-sm-10">
                                <input v-model="value['queries'][n]" type="text" class="form-control" :id="'label'+ key + n" placeholder="Add additional term">
                            </div>
                            <span @click="remove(key, n)" class="glyphicon glyphicon-remove" style="color:red; font-size:20px; margin-top:5px;"></span>
                        </div>

                    </div>
                </form>
            </div>
        </div>

         
        <button class="btn btn-primary" type="button" @click="build()">Build query!</button>
        
    </div>
</template>

<script>
    export default {
        data: function(){
            return{
                filters:{
                    "text":{
                        "queries": [],
                        "amount": 0
                    },
                    "label":{
                        "queries": [],
                        "amount": 0
                    },
                    "title":{
                        "queries": [],
                        "amount": 0
                    },
                    "year":{
                        "queries": [],
                        "amount": 0
                    },
                    "author":{
                        "queries": [],
                        "amount": 0
                    }
                }
            }
        },
        mounted() {
            console.log('Component mounted.')
        },
        methods: {
            build(){
                var query = '';
                for (var cat in this.filters){
                    if (this.filters[cat]['queries'].length > 0){
                        if (cat != "text"){
                            query += cat + ':\"' + this.filters[cat]['queries'].join('","') + '\" ';
                        }
                        else{
                            query += " " + this.filters[cat]['queries'].join(" ") + " ";
                        }
                        this.filters[cat]['queries'] = [];
                        this.filters[cat]['amount'] = 0;
                    }
                }
                window.location.replace('/search?q=' + query);
            },
            remove(cat, index){
                this.filters[cat]['queries'].splice(index, 1)
                this.filters[cat]['amount'] -= 1;
            }
        }
    }
</script>
