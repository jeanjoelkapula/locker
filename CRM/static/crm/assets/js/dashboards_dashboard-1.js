/**/
//csrf token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$(function() {
  $('#pipeline-selection').on('change', (evt)=> {
    const request = new Request(
        `/stage/${evt.target.value}/stats`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    fetch(request, {
        method: 'GET',
        "mode": "same-origin"
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.log(data.error);
        }

        if (data.success) {
            body = document.querySelector('#stage-stats-body');
            body.innerHTML = "";
            data.stats.forEach(element => {
              tr = document.createElement('tr');
              tr.innerHTML = `
                <td>${element.name}</td>
                <td>${element.count} Leads</td>
                <td>$${element.value}</td>
              `;
              body.append(tr);
            });

        }
        
    })
    .catch(error => {
        console.log( error);
    });
  });


  var chart1 = new Chart(document.getElementById('statistics-chart-1').getContext("2d"), {
    type: 'line',
    data: {
      labels: stat_chart_data.labels,
      datasets: stat_chart_data.datasets,
    },
    options: {
      scales: {
        xAxes: [{
          gridLines: {
            display: false
          },
          ticks: {
            fontColor: '#aaa'
          }
        }],
        yAxes: [{
          gridLines: {
            display: false
          },
          ticks: {
            fontColor: '#aaa',
            stepSize: 20
          }
        }]
      },

      responsive: true,
      maintainAspectRatio: false
    }
  });


  var chart5 = new Chart(document.getElementById('statistics-chart-5').getContext("2d"), {
    type: 'doughnut',
    data: {
      datasets: doughnut_chart_data
    },

    options: {
      scales: {
        xAxes: [{
          display: false,
        }],
        yAxes: [{
          display: false
        }]
      },
      legend: {
        display: false
      },
      tooltips: {
        enabled: false
      },
      cutoutPercentage: 94,
      responsive: true,
      maintainAspectRatio: false
    }
  });

  var chart6 = new Chart(document.getElementById('statistics-chart-6').getContext("2d"), {
    type: 'pie',
    data: {
      labels: leads_pie_chart_data.labels,
      datasets: leads_pie_chart_data.datasets
    },

    options: {
      scales: {
        xAxes: [{
          display: false,
        }],
        yAxes: [{
          display: false
        }]
      },
      legend: {
        position: 'right',
        labels: {
          boxWidth: 12
        }
      },
      responsive: false,
      maintainAspectRatio: false
    }
  });

  //new PerfectScrollbar(document.getElementById('tasks-inner'));
  //new PerfectScrollbar(document.getElementById('team-todo-inner'));

  if ($('html').attr('dir') === 'rtl') {
    $('#sales-dropdown-menu').removeClass('dropdown-menu-right');
  }

  // Resizing charts

  function resizeCharts() {
    chart1.resize();
    chart5.resize();
    chart6.resize();
  }

  // Initial resize
  resizeCharts();

  // For performance reasons resize charts on delayed resize event
  window.layoutHelpers.on('resize.dashboard-1', resizeCharts);
});
