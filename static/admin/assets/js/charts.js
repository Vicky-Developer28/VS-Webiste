<script>
// Get the data from Django context
var solar_dates = {{ solar_dates  |safe }};
var solar_values = {{ solar_values|safe }};

var cctv_dates = {{ cctv_dates|safe }};
var cctv_values = {{ cctv_values|safe }};

var whatsapp_dates = {{ whatsapp_dates|safe }};
var whatsapp_values = {{ whatsapp_values|safe }};

// Solar Data Chart
var ctx1 = document.getElementById('solarChart').getContext('2d');
var solarChart = new Chart(ctx1, {
  type: 'line',
  data: {
    labels: solar_dates,
    datasets: [{
      label: 'Solar Data',
      data: solar_values,
      borderColor: 'rgba(75, 192, 192, 1)',
      tension: 0.1,
      fill: false
    }]
  }
});

// CCTV Data Chart
var ctx2 = document.getElementById('cctvChart').getContext('2d');
var cctvChart = new Chart(ctx2, {
  type: 'line',
  data: {
    labels: cctv_dates,
    datasets: [{
      label: 'CCTV Data',
      data: cctv_values,
      borderColor: 'rgba(255, 99, 132, 1)',
      tension: 0.1,
      fill: false
    }]
  }
});

// WhatsApp Enquiry Request Chart
var ctx3 = document.getElementById('whatsappChart').getContext('2d');
var whatsappChart = new Chart(ctx3, {
  type: 'line',
  data: {
    labels: whatsapp_dates,
    datasets: [{
      label: 'WhatsApp Enquiry Requests',
      data: whatsapp_values,
      borderColor: 'rgba(153, 102, 255, 1)',
      tension: 0.1,
      fill: false
    }]
  }
});
</script>