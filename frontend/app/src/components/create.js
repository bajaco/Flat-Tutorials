import React, { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react';
import { Redirect } from 'react-router-dom';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

const Create = () => {
  const { getAccessTokenSilently } = useAuth0(); 
  const [ title, setTitle ] = useState('');
  const [ tags, setTags ] = useState('');
  const [ text, setText ] = useState('');
  const [ apiResponse, setApiResponse ] = useState();

  const submit = (event) => {
    event.preventDefault();
    if (title && tags && text) {
      (async () => {
        try {
          const token = await getAccessTokenSilently({
            audience: 'http://localhost:5000/',
            scope: 'submit:tutorial',
          });
          const response = await fetch('http://localhost:5000/submit', {
            method: 'POST',
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
  
  if (apiResponse) {
    return(
      <Redirect to='/' />
    );
  }

  return(

    <Form onSubmit={submit}>
      <Form.Group controlId="formTitle">
        <Form.Label>Title</Form.Label>
        <Form.Control type="text" value={title} onChange={e => setTitle(e.target.value)} placeholder="Enter title" />
      </Form.Group>
      <Form.Group controlId="formTags">
        <Form.Label>Tags</Form.Label>
        <Form.Control type="text" value={tags} onChange={e => setTags(e.target.value)} placeholder="Enter tags" />
        <Form.Text className="text-muted">
          e.g. Flask, Python, React
        </Form.Text>
      </Form.Group>

      <Form.Group controlId="formTutorial">
        <Form.Label>Tutorial</Form.Label>
        <Form.Control as="textarea" value={text} onChange={e => setText(e.target.value)} rows={20} placeholder="Write tutorial here" />
      </Form.Group>
      <Button variant="outline-dark" type="submit">
        Submit
      </Button>
    </Form>
  );
}
export default Create;
