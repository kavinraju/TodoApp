
        const checkboxes = document.querySelectorAll('.check-completed');
        for(let i=0; i < checkboxes.length; i++){
            
            const checkbox = checkboxes[i];
            setCheckboxlistener(checkbox);
        }


        document.getElementById('form').onsubmit = function(e) {
            e.preventDefault();
            fetch(
                '/todos/create', {
                    method: 'POST',
                    body: JSON.stringify({
                        'description': document.getElementById('description').value
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }
            ).then(function(response){
                console.log(response)
                return response.json();
            }).then(function(jsonResponse){
                console.log(jsonResponse);
                
                const liItem = document.createElement('li');
                const container = document.createElement('div');
                const inputItem = document.createElement('input');

                inputItem.setAttribute("type", "checkbox");
                inputItem.id = "checkbox_todo_completed";
                inputItem.className = "check-completed";
                inputItem.checked = jsonResponse['completed'];
                inputItem.setAttribute('data-id', jsonResponse['todo_id'])
                setCheckboxlistener(inputItem)
                
                container.appendChild(inputItem)
                container.appendChild(document.createTextNode(jsonResponse['description']))
                liItem.appendChild(container)

                document.getElementById('todos').appendChild(liItem)
                document.getElementById('error').className = 'hidden'
            }).catch(function(){
                document.getElementById('error').className = ''
            })
        }

        function setCheckboxlistener(checkbox){
            checkbox.onchange = function(e) {
                console.log(e);
                const newCompleted  = e.target.checked;
                const todoId = e.target.dataset['id']
                fetch('/todos/' + todoId + '/set-completed',{
                    method: 'POST',
                    body:JSON.stringify({
                        'completed':newCompleted,
                    }),
                    headers:{
                        'Content-Type':'application/json'
                    }
                }).then(function(){
                    document.getElementById('error').className = 'hidden'
                }).catch(function(e){
                    console.error(e);
                    
                    document.getElementById('error').className = ''
                })
            }
        }