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

        $("#form-usuario").on("submit", function(){
            let csrftoken = $("[name=csrfmiddlewaretoken]").val();
            $('#btn-form-usuario').html('Guardando...');
            $.ajax({
                url: $("#form-usuario").attr('data-url'),
                type: 'POST',
                data: $("#form-usuario").serialize(),
                headers:{
                    "X-CSRFToken": csrftoken
                },
                success:function(data){
                    if(data.respuesta=='ok'){
                        $('#btn-form-usuario').html('Guardado');
                        $('#modal_usuario').hide();
                        location.reload();
                        $('#div-errores').hide();
                    }
                    else{//data.respuesta=='error'
                        $('#id_error').html('');
                        $('#id_error').html(data.mensaje);
                        $('#btn-form-usuario').html('Guardado');
                        $('#div-errores').show();
                    }
                }
            });
            return false;
        });

        $('#div-errores').hide();

        $("#form-editar-usuario").on("submit", function(){
            let csrftoken = $("[name=csrfmiddlewaretoken]").val();
            $('#btn-form-editar-usuario').html('Guardando...');
            $.ajax({
                url: $("#form-editar-usuario").attr('data-url'),
                type: 'POST',
                data: $("#form-editar-usuario").serialize(),
                headers:{
                    "X-CSRFToken": csrftoken
                },
                success:function(data){
                    if(data.respuesta=='ok'){
                        $('#btn-form-editar-usuario').html('Guardado');
                        $('#modal_editar_usuario').hide();
                        location.reload();
                        $('#div-errores').hide();
                    }
                    else{//data.respuesta=='error'
                        $('#id_error').html('');
                        $('#id_error').html(data.mensaje);
                        $('#btn-form-editar-usuario').html('Guardado');
                        $('#div-errores').show();
                    }
                }
            });
            return false;
        });

    });

});