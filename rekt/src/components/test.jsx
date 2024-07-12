import React from 'react';
import axios from 'axios';

export default class Heh extends React.Component {
    
  state = {
    woo: []
  }

  componentDidMount() {
    axios.get(`http://localhost:8000/api/hello-react`)
      .then(res => {
        const persons = res.data;
        this.setState({ persons });
        console.log(res.data)
      })
  }

  render() {
    return (
      <ul>
        {
          this.state.persons
        }
      </ul>
    )
  }
}