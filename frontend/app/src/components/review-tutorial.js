import React, { useEffect, useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { Link, useParams, Redirect } from 'react-router-dom';
import Badge from 'react-bootstrap/Badge';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import ReactMarkdown from 'react-markdown';


const ReviewTutorial = () => {
  const { getAccessTokenSilently } = useAuth0();
  const [ tutorial, setTutorial ] = useState();
  const [ notes, setNotes ] = useState();
  const [ apiResponse, setApiResponse ] = useState();
  const [ submitted, setSubmitted ] = useState(false);
  const { tutorialid } = useParams();
  
  useEffect(() => {
    (async () => {
      try {
        const token = await getAccessTokenSilently({
          audience: process.env.REACT_APP_AUDIENCE,
          scope: 'view:unpublished',
        });
        const response = await fetch(process.env.REACT_APP_API_URL + '/unpublished/' + tutorialid, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setTutorial(await response.json());
      } catch(e) {
        console.error(e);
      }
    })();
  }, [getAccessTokenSilently, tutorialid]);

  const approve = (event) => {
    event.preventDefault();
    if (!submitted) { 
      console.log('approve');
      setSubmitted(true);
      (async () => {
        try {
          const token = await getAccessTokenSilently({
            audience: process.env.REACT_APP_AUDIENCE,
            scope: 'submit:tutorial',
          });
          const response = await fetch(process.env.REACT_APP_API_URL + '/publish/' + tutorialid, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
          });
          setApiResponse(await response.json());
        } catch (e) {
          console.log(e);
        }
      })();
    } 
  }
  
  const deny = (event) => {
    event.preventDefault();
    if (!submitted) {
      console.log('deny');
      setSubmitted(true);
      (async () => {
        try {
          const token = await getAccessTokenSilently({
            audience: process.env.REACT_APP_AUDIENCE,
            scope: 'submit:tutorial',
          });
          const response = await fetch(process.env.REACT_APP_API_URL + '/deny/' + tutorialid, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              reviewer_notes: notes,
            }),
          });
          setApiResponse(await response.json());
        } catch (e) {
          console.log(e);
        }
      })();
    }
  }
  
  if (apiResponse) {
    return (
      <Redirect to='/review' />
    );
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
      <Form>
        <Form.Group controlId="formNotes">
          <Form.Label>Enter notes if rejecting tutorial.</Form.Label>
          <Form.Control as="textarea" value={notes} onChange={(e => setNotes(e.target.value))} rows={5} placeholder="Enter rejection notes" />
        </Form.Group>
        <Button variant="outline-dark" type="submit" onClick={approve}>
          Approve
        </Button>
        <Button variant="outline-dark" type="submit" onClick={deny}>
          Reject
        </Button>
      </Form>
    </>
  );
  
}
export default ReviewTutorial
