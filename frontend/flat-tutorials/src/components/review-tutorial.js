import React, { useEffect, useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { Link, useParams } from 'react-router-dom';
import Badge from 'react-bootstrap/Badge';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import ReactMarkdown from 'react-markdown';


const ReviewTutorial = () => {
  const { getAccessTokenSilently } = useAuth0();
  const [ tutorial, setTutorial ] = useState();
  const [ notes, setNotes ] = useState();
  const { tutorialid } = useParams();
  
  useEffect(() => {
    (async () => {
      try {
        const token = await getAccessTokenSilently({
          audience: 'http://localhost:5000/',
          scope: 'view:unpublished',
        });
        const response = await fetch('http://localhost:5000/unpublished/' + tutorialid, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setTutorial(await response.json());
      } catch(e) {
        console.error(e);
      }
    })();
  }, [getAccessTokenSilently]);

  const submit = (event) => {
    console.log('ok...');
  }

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
    <>
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
      <Form onSubmit={submit}>
        <Form.Group controlId="formNotes">
          <Form.Label>Enter notes if rejecting tutorial.</Form.Label>
          <Form.Control as="textarea" value={notes} onChange={(e => setNotes(e.target.value))} rows={5} placeholder="Enter rejection notes" />
        </Form.Group>
        <Button variant="outline-dark" type="submit" value="approve">
          Approve
        </Button>
        <Button variant="outline-dark" type="submit" value="reject">
          Reject
        </Button>
      </Form>
    </>
  );
  
}
export default ReviewTutorial
