import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom';
import Badge from 'react-bootstrap/Badge';


const TagsTutorials = () =>{
  const [ tutorials, setTutorials ] = useState()
  const { tagname } = useParams();
  useEffect(() => {
    
    (async () => {
      try {
        
        const response = await fetch(process.env.REACT_APP_API_URL + '/published/tags/' + tagname);
        setTutorials(await response.json());
      } catch(e) {
        console.error(e);
      }
    })();
  }, [tagname]);

  if (!tutorials) {
    return (
      <div class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    )
  } else if (!tutorials['success']) {
    return(
      <h3>No tutorials found!</h3>
    );
  } else {
    return (
      <div id="tutorials-list"> 
        {tutorials['tutorials'].map((tutorial) => (
          <div class="card mb-sm-2">
            <div class="card-body d-flex flex-row justify-content-between">
              <Link class='text-dark' to={'/tutorials/' + tutorial.id}>
                <h5 class="card-title">{tutorial.title}</h5>
              </Link>
              
            </div>
            <div class='card-footer d-flex flex-row justify-content-between'>
              <div>
              {tutorial['tags'].map((tag) => (       
                <>
                  <Link to={'/tags/' + tag}>
                    <Badge variant='dark'>
                      {tag}
                    </Badge>
                  </Link>
                  {' '}
                </>
              ))}
              </div>
              <i>by {tutorial.author}  </i>
            </div>
          </div>
        ))}
      </div>
    );
  }
}
export default TagsTutorials;
