import React, { Component } from 'react';
import Typekit from 'react-typekit';
import './style/resume.css';
// import resumeContent from './resource/resumeContent.json';
import resumeContent from './resource/tmpdata.json';

// import jsPDF from 'jspdf'

function importAll(r) {
  let images = {};
  r.keys().map((item, index) => { images[item.replace('./', '')] = r(item); });
  return images;
}
const apps = importAll(require.context('./resource/apps', false, /\.(png|jpe?g|svg)$/));

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
              <span id="web"><a href={"http://www." + this.props.contact.web}>{this.props.contact.web}</a></span>
              <span id="email"><a href={"mailto:"+this.props.contact.email}>{this.props.contact.email}</a></span>
              <span id="phone"><a href={"tel:"+this.props.contact.phone}>{this.props.contact.phone}</a></span>
            </div>
          </div>
          <div id="tagline">{this.props.tagline[0]}</div>
        </div>
      </header>
    )
  }
};

function SectionHeader(props) {
  return (
    <h1 className="section-header">
      {props.id}
    </h1>
  )
}

class List extends Component{
  render() {
    var list = this.props.list
    var limit = this.props.limit
    var ListItems = Object.keys(list).map(function(key){
      if (!(key >= limit))
        return <li><span>{list[key]}</span></li>
    });
    return (
      <ul className="list-content">{ListItems}</ul>
    )
  };
}

class WorkList extends Component {
  render() {
    var jobs = this.props.items
    var limit = this.props.limit
    var bulletLimit = this.props.bulletLimit
    var ListItems = Object.keys(jobs).map(function(key){
      if (jobs[key].company == 'Sony')
        bulletLimit -= 1
      if (!(key >= limit))
        return (
          <article className="job" id={jobs[key].company.toLowerCase()}>
            <div className="item-header">
              <span className="title item-position">
                {jobs[key].position}
              </span>
              <span className="title item-title">
                <a href={"http://"+ jobs[key].url}>
                  {jobs[key].company}
                </a>
              </span>
              <span className="item-duration">
                {jobs[key].term}
              </span>
              <span className="item-location">
                {jobs[key].location} 
              </span>
            </div>
            <div className="content">
              <List list={jobs[key].responsibilities} limit={bulletLimit}/>
            </div>
          </article>
        )
    });
    return (
      <div>{ListItems}</div>
    )
  };
}

class ProjectList extends Component {
  render() {
    var projects = this.props.items
    var limit = this.props.limit
    var bulletLimit = this.props.bulletLimit
    var ListItems = Object.keys(projects).map(function(key){
      if (!(key >= limit))
        return (
          <article className="project" id={projects[key].id.toLowerCase()}>
            <div className="item-header">
              <span className="item-title">
                <a href={"http://" + projects[key].url}>
                  {projects[key].name}
                </a>
              </span>
              <span className="item-duration">
                {projects[key].term}
              </span>
            </div>
            <div className="content">
              <div className="description">
                {projects[key].description}
              </div>
              <List list={projects[key].responsibilities} limit={bulletLimit}/>
            </div>
          </article>
        )
    });
    return (
      <div>{ListItems}</div>
    )
  };
}

class SkillsList extends Component {
  render() {
    var skills = this.props.items
    var limit = Number(this.props.limit)
    var ListItems = Object.keys(skills).map(function(key){
      if (!(key >= limit)) {
        var id = skills[key].toLowerCase()
        return (
          <li className="resume-item">
            <div className="app-logo" id={id}>
              <img src={apps[id + ".png"]}/>
            </div>
            <p className="app-name">{skills[key]}</p>
          </li>
        )
      }
    });
    return (
      <ul>{ListItems}</ul>
    )
  }
}

class AwardList extends Component {
  render() {
    var awards = this.props.items
    var limit = this.props.limit
    var ListItems = Object.keys(awards).map(function(key){
      if (!(key >= limit)) {
        var id = awards[key][0].toLowerCase()
        return (
          <article>
            <div className="item-header">
              <span className="item-title">
                {awards[key].name}
              </span>
            </div>
          </article>
        )
      }
    });
    return(
      <div>{ListItems}</div>
    )
  }
}

function Summary(props) {
  return (
    <section id="summary">
      <SectionHeader id="Summary"/>
      <List list={props} limit="3"/>
    </section>
  )
}

function Experience(props) {
  return (
    <section id="experience">
      <SectionHeader id="Experience"/>
      <WorkList items={props} limit="4" bulletLimit="3"/>
    </section>
  )
}

function Projects(props) {
  return (
    <section id="projects">
      <SectionHeader id="Projects"/>
        <ProjectList items={props} limit="4" bulletLimit="2"/>
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
      <SkillsList items={props} limit="11"/>
    </section>
  )
}

function Education(props) {
  var school = props[0]
  return (
    <section id="education">
      <SectionHeader id="Education"/>
      <article className="school" id={school.id}>
          <div className="item-header">
            <span className="title item-position">
              <a href={"http://"+ school.url}>
                {school.school}
              </a>
            </span>
            <span className="title item-title">
                {school.program}
              <span id="degree">
                {school.degree}
              </span>
            </span>
            <span id="minor">
                {school.minor}
              </span>
            <span className="item-duration">
              {school.class}
            </span>
          </div>
        </article>
    </section>
  )
}

function Awards(props) {
  <section id="awards">
    <SectionHeader id="Awards"/>
    <AwardList items={props} limit="3"/>
  </section>
}

function Interests(props) {
  return (
    <section id="interests">
      <SectionHeader id="Interests"/>
      <List list={props} limit="2"/>
    </section>
  )
}

function Resume(props) {
  return(
    <div>
      <Header {...props.bio}/>
      <Summary {...props.summary} /> 
      <Experience {...props.experience} />
      <Projects {...props.projects} />
      <Clubs {...props.clubs} />
      <Education {...props.education} />
      <Skills {...props.skills} />
    </div>
  )
}

class App extends Component {
  // constructor(props) {
  //     super(props);
  //     this.pdfToHTML=this.pdfToHTML.bind(this);
  // }

  componentDidMount() {
    // window.print()
    // this.pdfToHTML()
    // console.log(document.documentElement)
    // Prince().input(document.documentElement.outerHTML)
  }

  // pdfToHTML() {
  //   console.log("PDF")
  //   var pdf = new jsPDF('p', 'pt', 'letter');
  //   // source needs to have css in it
  //   var source = document.documentElement;
  //   console.log(source)
  //   var specialElementHandlers = {
  //     '#bypassme': function(element, renderer) {
  //       return true
  //     }
  //   };

  //   var margins = {
  //     // top: 50,
  //     // left: 60,
  //     // width: 545
  //   };

  //   pdf.fromHTML (
  //     source // HTML string or DOM elem ref.
  //     , margins.left // x coord
  //     , margins.top // y coord
  //     , {
  //         'width': margins.width // max width of content on PDF
  //         , 'elementHandlers': specialElementHandlers
  //       },
  //     function (dispose) {
  //       // dispose: object with X, Y of the last line add to the PDF
  //       // this allow the insertion of new lines after html
  //       pdf.save('html2pdf.pdf');
  //     }
  //   )
  // }

  render() {
    return (
      <div>
        <Typekit kitId="onu2sfw" />
        <Resume {...resumeContent}/>
      </div>  
    );
  }
}

export default App;