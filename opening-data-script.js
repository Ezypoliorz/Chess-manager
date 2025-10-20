document.addEventListener('DOMContentLoaded', function() {
  const ctx = document.getElementById('chart1');

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Parties gagnées', 'Parties perdues', 'Parties nulles'],
      datasets: [{
        label: 'Statistiques des parties',
        data: [67, 30, 3], // Vos données dynamiques
        backgroundColor: [
          'rgb(75, 192, 192)',
          'rgb(255, 99, 132)',
          'rgb(255, 205, 86)'
        ],
        hoverOffset: 4,
        borderRadius: 20,
        spacing:10
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      layout: {
            padding: {
                left: 10,
                right: 10,
                top: 10,
                bottom: 10
            }
        },
      plugins: {
        tooltip: {
          enabled: false
        },
        legend: {
          display:false,
          position: 'top',
        },
        title: {
          display: false,
          text: 'Répartition des résultats'
        }
      },
      cutout: '65%'
    }
  });
});

// Function to load the JSON openings data
    async function loadJsonData(filePath) {
    try {
        // Retrieving JSON content
        const response = await fetch(filePath);

        // Checking for errors
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        // Formatting the data
        const data = await response.json();
        console.log("JSON data :");
        console.log(data);

        return data;
    } catch (error) {
        console.error("Impossible de charger ou de traiter le fichier JSON :", error);
    }
}

var profile_url = ''
var opening_name = 'Sicilian Defense'
// Function to create the player's ratings graphs
    document.addEventListener('DOMContentLoaded', async function() {
        const data = await loadJsonData("player_data.json");
        ratings = []
        if (data) {
            profile_url = `https://www.chess.com/member/${data["Username"].toLowerCase()}/stats`;
            document.getElementById('UsernameText').textContent = data["Username"];
            document.getElementById('NameText').textContent = data["Name"];
            document.getElementById('ProfilePicture').src = data["Avatar"];
            //Rapid Graph
                var ratings = data["Rapid"].slice(-200);
                var ctx = document.getElementById("ChartRapidRating");
                var labels = ratings.map((_, index) => `Game ${index + 1}`);
                new Chart(ctx , {
                    type : 'line',
                    data : {
                    labels : labels,
                    datasets : [{
                        label : false,
                        data : ratings,
                        fill : false,
                        borderColor : 'rgb(75, 192, 192)',
                        pointStyle : false,
                        tension : 0.1
                    }]
                    },
                    options : {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                        tooltip: {
                        enabled: true
                        },
                        legend: {
                        display:false,
                        position: 'top',
                        },
                        title: {
                        display: false,
                        text: ''
                        }
                    },
                    scales: {
                                x: {
                                    ticks: {
                                        display : false
                                    },
                                    grid : {
                                        display : false
                                    }
                                }
                            }
                    }
                });

            // Blitz graph
                ratings = data["Blitz"].slice(-200);
                ctx = document.getElementById("ChartBlitzRating");
                labels = ratings.map((_, index) => `Game ${index + 1}`);
                new Chart(ctx , {
                    type : 'line',
                    data : {
                    labels : labels,
                    datasets : [{
                        label : false,
                        data : ratings,
                        fill : false,
                        borderColor : 'rgb(75, 192, 192)',
                        pointStyle : false,
                        tension : 0.1
                    }]
                    },
                    options : {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                        tooltip: {
                        enabled: true
                        },
                        legend: {
                        display:false,
                        position: 'top',
                        },
                        title: {
                        display: false,
                        text: ''
                        }
                    },
                    scales: {
                                x: {
                                    ticks: {
                                        display : false
                                    },
                                    grid : {
                                        display : false
                                    }
                                }
                            }
                    }
                });

            // Bullet graph
                ratings = data["Bullet"].slice(-200);
                ctx = document.getElementById("ChartBulletRating");
                labels = ratings.map((_, index) => `Game ${index + 1}`);
                new Chart(ctx , {
                    type : 'line',
                    data : {
                    labels : labels,
                    datasets : [{
                        label : false,
                        data : ratings,
                        fill : false,
                        borderColor : 'rgb(75, 192, 192)',
                        pointStyle : false,
                        tension : 0.1
                    }]
                    },
                    options : {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            tooltip: {
                                enabled: true
                            },
                            legend: {
                                display:false,
                                position: 'top',
                            },
                            title: {
                                display: false,
                                text: ''
                            },
                        },
                        scales: {
                                x: {
                                    ticks: {
                                        display : false
                                    },
                                    grid : {
                                        display : false
                                    }
                                }
                            }
                    }
                });
        };

        const data_opening = await loadJsonData("openings_winrate.json");
        if (data_opening){
            let winrate_evolution_list = null
            const selected_data_opening = data_opening.find(
                (item) => item["Opening-Name"] == opening_name
            );
            if (selected_data_opening) {
                winrate_evolution_list = selected_data_opening["Winrate-Evolution"];
                console.log(winrate_evolution_list);
            }
            var labels = winrate_evolution_list.map((_, index) => `Game ${index + 1}`);
            let dataset_data = [];
            let dataset_background_color = [];
            let dataset_border_color = [];
            for (const game of winrate_evolution_list) {
                dataset_data.push(game["Winrate"])
                if (game["Result"] === "Win") {
                    dataset_background_color.push('rgba(104, 255, 99, 0.5)');
                    dataset_border_color.push('rgba(104, 255, 99, 1)');
                }
                else {
                    dataset_background_color.push('rgba(255, 99, 132, 0.5)');
                    dataset_border_color.push('rgba(255, 99, 132, 1)');
                }
            };
            const data = {
                labels: labels,
                
                datasets: [{
                    label: 'Winrate Evolution',
                    data: dataset_data,
                    backgroundColor: dataset_background_color,
                    borderColor: dataset_border_color,
                    borderWidth: 1
                }]
            };
            const config = {
                type: 'bar',
                data: data,
                options : {
                                    responsive: true,
                                    maintainAspectRatio: false,
                                    plugins: {
                                    tooltip: {
                                    enabled: true
                                    },
                                    legend: {
                                    display:false,
                                    position: 'top',
                                    },
                                    title: {
                                    display: false,
                                    text: ''
                                    }
                                },
                                scales: {
                                            x: {
                                                ticks: {
                                                    display : false
                                                },
                                                grid : {
                                                    display : false
                                                }
                                            }
                                        }
                                }
            };
            const ctx = document.getElementById('WinrateChartEvolution').getContext('2d');

            const myChart = new Chart(
                ctx,
                config
            );
        };
    });


// Redirecting to the profile page when the button is clicked
    document.getElementById('ProfileButton').addEventListener('click', () => {
        window.open(profile_url, '_blank');
    });