<template>
    <div id="myNetwork" style="height:500px;">
    </div>
</template>

<script>
    export default {
        mounted() {
            var url = window.location.href;
            var regex = /authors\/(\d+)/;
            var author_id = regex.exec(url)[1];

            axios.post('/api/get-author-graph', {
                author_id: author_id
            })
            .then(response => this.draw(response.data))
            .catch(error => console.log(error));
        },
        methods: {
            draw(data){
                console.log(data);
                var container = document.getElementById('myNetwork');
                var data = {
                    nodes: data['nodes'],
                    edges: data['edges']
                };
                var options = {
                    autoResize: true,
                    nodes: {
                      scaling:{
                        label: {
                          min:12,
                          max:20
                        }
                      },
                      borderWidth:1,
                      color: {
                        border: '#222222',
                      },
                      font:{color:'#eeeeee'}
                    },
                    edges: {
                      color: 'lightgray'
                    },
                    interaction: {
                        navigationButtons: true
                    },
                    physics: {
                        solver: 'barnesHut',
                        barnesHut: {
                            avoidOverlap: 0.3,
                        },
                        stabilization: {
                            iterations: 10,
                            updateInterval: 2000
                        }
                    }
                };
                var network = new vis.Network(container, data, options);
                network.on("doubleClick", function (params) {
                    if (params['nodes'].length > 0){
                        window.location.replace('/authors/' + params['nodes'][0])
                    }
                });
            }
        }
    }
</script>
