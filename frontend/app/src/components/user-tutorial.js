import React, { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react';
import { Redirect, useParams, Link } from 'react-router-dom';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import Card from 'react-bootstrap/Card';
import Badge from 'react-bootstrap/Badge';
import Alert from 'react-bootstrap/Alert';
import ReactMarkdown from 'react-markdown';

const UserTutorial = () => {
  const { getAccessTokenSilently } = useAuth0(); 
  const [ title, setTitle ] = useState();
  const [ tags, setTags ] = useState();
  const [ text, setText ] = useState();
  const [ tutorial, setTutorial ] = useState();
  const [ submitted, setSubmitted ] = useState(false);
  const { tutorialid } = useParams();
  const [ apiResponse, setApiResponse ] = useState();

  useEffect(() => {
    (async () => {
      try {
        const token = await getAccessTokenSilently({
          audience: 'http://localhost:5000/',
          scope: 'submit:tutorial',
        });

        const response = await fetch('http://localhost:5000/submitted/' + tutorialid, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const json = await response.json();
        setTutorial(json);
        setTitle(json['tutorial']['title']);
        setTags(json['tutorial']['tags'].join(', '));
        setText(json['tutorial']['text']);
        
      } catch(e) {
        console.error(e);
      }
    })();
  }, [getAccessTokenSilently]);
  

  const submit = (event) => {
    event.preventDefault();
    if (!submitted) {
      setSubmitted(true);
      if (title && tags && text) {
        (async () => {
          try {
            const token = await getAccessTokenSilently({
              audience: 'http://localhost:5000/',
              scope: 'edit:tutorial',
            });
            const response = await fetch('http://localhost:5000/edit/' + tutorialid, {
              method: 'PATCH',
              headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
              },
              body: JSON.stringify({
                title: title,
                tags: tags,
                text: text
              })
            });
            setApiResponse(await response.json());
          } catch (e) {
            console.log(e);
          }
        })();
      }
    }
  }
  
  const tagstring = () => {
    return tags.split(', ');
  }

  if (apiResponse) {
    return(
      <Redirect to='/my-tutorials' />
    );
  }

  if (!(tutorial && title && text && tags)) {
    return (
      <div class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    )
  } else { 
    return(
      <>
        {!tutorial['tutorial']['under_review'] && !tutorial['tutorial']['published'] &&
          <Alert variant="danger">
            <Alert.Heading>Sorry, your tutorial was rejected.</Alert.Heading>
            <p>{tutorial['tutorial']['reviewer_notes']}</p>
          </Alert>
        }
        <Tabs defaultActiveKey="view">
          <Tab eventKey="view" title="View" class="text-dark">
            <Card>  
              <Card.Body>
                <Card.Title>
                  {title}
                </Card.Title>
                <Card.Text>
                  <ReactMarkdown>
                    {text}
                  </ReactMarkdown>
                </Card.Text>
              </Card.Body>
              <Card.Footer>
               {tags.split(', ').map((tag) => (
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
          </Tab>
          <Tab eventKey="edit" title="Edit">
            <Form onSubmit={submit}>
              <Form.Group controlId="formTitle">
                <Form.Label>Title</Form.Label>
                <Form.Control type="text" onChange={e => setTitle(e.target.value)} 
                  defaultValue = {title} />
              </Form.Group>
              
              <Form.Group controlId="formTags">
                <Form.Label>Tags</Form.Label>
                <Form.Control type="text" defaultValue={tags} 
                  onChange={e => setTags(e.target.value)} />
                <Form.Text className="text-muted">
                  e.g. Flask, Python, React
                </Form.Text>
              </Form.Group>

              <Form.Group controlId="formTutorial">
                <Form.Label>Tutorial</Form.Label>
                <Form.Control as="textarea" defaultValue={text} 
                  onChange={e => setText(e.target.value)} rows={20} />
              </Form.Group>
              <Button variant="outline-dark" type="submit">
                Submit Changes
              </Button>
            </Form>
          </Tab>
        </Tabs>
      </>
    );
  }
}
export default UserTutorial;
