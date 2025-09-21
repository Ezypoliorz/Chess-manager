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