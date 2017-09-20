import React, { Component } from 'react';
import Typekit from 'react-typekit';
import './style/resume.css';
import resumeContent from './resource/resumeContent.json';

// -------- Header -------- //
class Header extends React.Component{
  render() {
    return (
      <header className="main-header">
        <div className="header">
          <div className="container">
            <div id="name">
              <a href="http://www.adamthompson.ca">
                {this.props.name.first} {this.props.name.last}
              </a>
            </div>
            <div id="contact">
              <span id="web"><a href="http://www.{this.props.contact.web}">{this.props.contact.web}</a></span>
              <span id="email"><a href="mailto:{this.props.contact.email}">{this.props.contact.email}</a></span>
              <span id="phone">{this.props.contact.phone}</span>
            </div>
          </div>
          <div class="tagline">{this.props.tagline[0]}</div>
        </div>
      </header>
    )
  }
};

function SectionHeader(props) {
  return (
    <h1 className="section-header">
      <div className="title section-title">{props.id}</div>
    </h1>
  )
}

class List extends Component{
  render() {
    var list = this.props.list
    var limit = this.props.limit
    var ListItems = Object.keys(list).map(function(key){
      if (!(key >= limit))
        return <li>{list[key].text}</li>
    });
    return (
      <ul>{ListItems}</ul>
    )
  };
}

class WorkList extends Component {
  render() {
    var jobs = this.props.items
    var limit = this.props.limit
    var ListItems = Object.keys(jobs).map(function(key){
      if (!(key >= limit))
        return (
          <article className="job" id="{jobs[key].company.toLowerCase()}">
            <div className="subsection-header">
              <span className="title subsection-company">
                <a href="http://{jobs[key].url}">
                  {jobs[key].company}
                </a>
              </span>
              <span className="title subsection-title">
                {jobs[key].position}
              </span>
              <span class="subsection-location">
                <span class ="subsection-location-before"> — </span>
                {jobs[key].location}
              </span>
              <span class="subsection-duration">
                {jobs[key].term}
              </span>
            </div>
            <List list={jobs[key].responsibilities} limit="4"/>
          </article>
        )
    });
    return (
      <ul>{ListItems}</ul>
    )
  };
}

class ProjectList extends Component {
  render() {
    var projects = this.props.items
    var limit = this.props.limit
    var ListItems = Object.keys(projects).map(function(key){
      if (!(key >= limit))
        return (
          <article className="job" id="{projects[key].id.toLowerCase()}">
            <div className="subsection-header">
              <span className="title subsection-title">
                <a href="http://{projects[key].url}">
                  {projects[key].name}
                </a>
              </span>
              <span className="subsection-duration">
                {projects[key].term}
              </span>
            </div>
            <div className="content">
              {projects[key].description}
            </div>
            <List list={projects[key].responsibilities} limit="4"/>
          </article>
        )
    });
    return (
      <ul>{ListItems}</ul>
    )
  };
}

class SkillsList extends Component {
  render() {
    var skills = this.props.items
    var limit = Number(this.props.limit)
    var ListItems = Object.keys(skills).map(function(key){
      if (!(key >= limit)) {
        return (
          <li className="resume-item" id={skills[key][0].toLowerCase()}>
            <div className="app-logo"></div>
            <p className="app-name">{skills[key][0]}</p>
          </li>
        )
      }
    });
    return (
      <ul>{ListItems}</ul>
    )
  }
}

function Summary(props) {
  return (
    <section id="summary">
      <SectionHeader id="Summary"/>
      <List list={props} limit="5"/>
    </section>
  )
}

function Experience(props) {
  return (
    <section id="experience">
      <SectionHeader id="Work Experience"/>
      <WorkList items={props} limit="3" />
    </section>
  )
}

function Projects(props) {
  return (
    <section id="projects">
      <SectionHeader id="Projects"/>
      <ProjectList items={props} limit="4" />
    </section>
  )
}

function Clubs(props) {
  return (
    <section id="clubs">
      <SectionHeader id="Clubs & Groups"/>
      <ProjectList items={props} limit="4" />
    </section>
  )
}

function Skills(props) {
  return (
    <section id="skills">
      <SectionHeader id="Toolbox"/>
      <SkillsList items={props} limit="8"/>
    </section>
  )
}

class App extends Component {
  render() {
    return (
      <div>
        <Typekit kitId="onu2sfw" />
        <Header {...resumeContent.bio}/>
        <Summary {...resumeContent.summary} /> 
        <Experience {...resumeContent.experience} />
        <Projects {...resumeContent.projects} />
        <Clubs {...resumeContent.clubs} />
        <Skills {...resumeContent.skills} />
      </div>
    );
  }
}

export default App;