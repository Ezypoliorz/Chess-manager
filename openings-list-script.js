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

// Creating new opening cards
    document.addEventListener('DOMContentLoaded', async function() {
    const data = await loadJsonData("openings_winrate.json");    
    if (data) {
        for (const element of data) {
        const opening = element['Opening-Name'];
        const winrate = element['Win-Rate'];
        const gamesPlayed = element['Total-Games'];
        const gamesWon = element.Wins;
        
        const divOpening = `
            <div class="div-opening"> 
                <h3 class="title-opening">${opening}</h3>
                <div class="div-content-opening">
                    <h3 class="content-opening">Winrate : ${winrate}</h3> 
                    <h3 class="content-opening">Games played : ${gamesPlayed}</h3> 
                    <h3 class="content-opening">Games won : ${gamesWon}</h3> 
                </div>
            </div>
        `;
        document.getElementById("DivOpeningsList").insertAdjacentHTML('beforeend', divOpening);
        }
    }
    });

var profile_url = ''
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
    });

// Redirecting to the profile page when the button is clicked
    document.getElementById('ProfileButton').addEventListener('click', () => {
        window.open(profile_url, '_blank');
    });