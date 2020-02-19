$(document).ready(function(){

    $(document).ready(function() {
        $('#table_datos').DataTable({
            "order": [],
            "language": {
                "lengthMenu": "Ver _MENU_ registros",
                "loadingRecords": "Loading...",
                "processing": "Processing...",
                "search": "Buscar:",
                "zeroRecords": "No se ha encontrado en la busqueda",
                "emptyTable": "No hay datos disponibles en la tabla",
                "info": "Visibles _START_ a _END_ de _TOTAL_ Registros",
                "infoEmpty": "Visibles 0 a 0 de 0 Registros",
                "paginate": {
                    "first": "Primera",
                    "last": "Última",
                    "next": "Siguiente",
                    "previous": "Anterior"
                }

            }

        });

        $('#div-errores').hide();

        $("#form-cliente").on("submit", function(){
            let csrftoken = $("[name=csrfmiddlewaretoken]").val();
            $('#btn-form-cliente').html('Guardando...');
            $.ajax({
                url: $("#form-cliente").attr('data-url'),
                type: 'POST',
                data: $("#form-cliente").serialize(),
                headers:{
                    "X-CSRFToken": csrftoken
                },
                success:function(data){
                    if(data.respuesta=='ok'){
                        $('#btn-form-cliente').html('Guardado');
                        $('#modal_cliente').hide();
                        location.reload();
                        $('#div-errores').hide();
                    }
                    else{//data.respuesta=='error'
                        $('#id_error').html('');
                        $('#id_error').html(data.mensaje);
                        $('#btn-form-cliente').html('Guardado');
                        $('#div-errores').show();
                    }
                }
            });
            return false;
        });

        $('#div-errores').hide();

        $("#form-edit-cliente").on("submit", function(){
            let csrftoken = $("[name=csrfmiddlewaretoken]").val();
            $('#btn-form-edit-cliente').html('Guardando...');
            $.ajax({
                url: $("#form-edit-cliente").attr('data-url'),
                type: 'POST',
                data: $("#form-edit-cliente").serialize(),
                headers:{
                    "X-CSRFToken": csrftoken
                },
                success:function(data){
                    if(data.respuesta=='ok'){
                        $('#btn-form-edit-cliente').html('Guardado');
                        $('#modal_editar_cliente').hide();
                        location.reload();
                        $('#div-errores').hide();
                    }
                    else{//data.respuesta=='error'
                        $('#id_error').html('');
                        $('#id_error').html(data.mensaje);
                        $('#btn-form-edit-cliente').html('Guardado');
                        $('#div-errores').show();
                    }
                }
            });
            return false;
        });


    });

});