import React, { useEffect, useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { Link, useParams } from 'react-router-dom';
import Badge from 'react-bootstrap/Badge';
import Card from 'react-bootstrap/Card';
import ReactMarkdown from 'react-markdown';

const PublicTutorial = () => {
 
  const [ tutorial, setTutorial ] = useState()
  const { tutorialid } = useParams();
  useEffect(() => {
    (async () => {
      try {
        const response = await fetch('http://localhost:5000/published/' + tutorialid);
        setTutorial(await response.json());
      } catch(e) {
        console.error(e);
      }
    })();
  }, [tutorialid]);

  if (!tutorial) {
    return (
      <div>
        <h1>loading . . .</h1>
      </div>
    )
  } else if (!tutorial['success']) {
    return (
      <h3>Not found.</h3>
    );
  }

  return (
    <Card>  
      <Card.Body>
        <Card.Title>
          {tutorial['tutorial']['title']}
        </Card.Title>
        <Card.Text>
          <ReactMarkdown>
            {tutorial['tutorial']['text']}
          </ReactMarkdown>
        </Card.Text>
      </Card.Body>
      <Card.Footer>
       {tutorial['tutorial']['tags'].map((tag) => (
          <>
            <Link to={'/tags/' + tag}>
              <Badge variant='dark'>
                {tag}
              </Badge>
            </Link>
          {' '}
          </>           
        ))}
      </Card.Footer>
    </Card>
  );
  
}
export default PublicTutorial
