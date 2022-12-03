/* function filtro() {
  const valor = document.getElementById("searchInput").value.toUpperCase();
  const nombres = document.getElementById("names");
  const filas = nombres.getElementsByTagName("tr");
  

  for(let i = 0; i < filas.length; i++){
    
    let rut = filas[i].getElementsByTagName("td")[1];

    let total = rut.textContent;

    filas[i].style.display = total.toUpperCase().indexOf(valor) > -1 ? "" : "none";
  }
  }

document.getElementById("searchInput").addEventListener("keyup", filtro);

 */
$(document).ready(function(){
  const table = $('#tableV').DataTable({
    orderCellsTop: true,
    fixedHeader: true  
  });
  $('#tableV thead tr:eq(1) th').clone(true).appendTo("#tableV thead");
  $('#tableV thead tr:eq(1) th').each( function (i) {
      const title = $(this).text();
      $(this).html('<input type="number" placeholder="buscar"/>');
      
      $(' input', this ).on( 'keyup change', function () {
          if (table.column(i).search() !== this.value) {
              table
                  .colum(i)
                  .search(this.value)
                  .draw();
          }
      })
  })

})

