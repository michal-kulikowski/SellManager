
  $(document).ready(function () {
        $('#table_fleet').DataTable({
            "ajax": {
                "url": "{% url 'panel_lokalizacji:lokalizacje_json' %}",
                "dataSrc": ""

            },
            "deferRender": true
        });
  });