import React, { Component } from 'react';
import Typekit from 'react-typekit';
import './style/resume-generator.css';
// import resumeContent from './resource/resumeContent.json';
import resumeContent from './resource/tmpdata.json';

// import jsPDF from 'jspdf'

function importAll(r) {
  let images = {};
  r.keys().map((item, index) => { images[item.replace('./', '')] = r(item); });
  return images;
}
const apps = importAll(require.context('./resource/apps', false, /\.(png|jpe?g|svg)$/));

// ================================================================================ //
// ================================================================================ //
// ==================================== Resume ==================================== //
// ================================================================================ //
// ================================================================================ //


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

// class CategoryList extends Component {
//   render(){
//     var type = this.props.type
//     var items = this.props.items
//     var limit = this.props.limit
//     var bulletLimit = this.props.bulletLimit

//     var ListItems = Object.keys(items).map(function(key){
//       if (!(key >= limit))
//         return(
//           <article className={type} id={projects[key].id.toLowerCase()}>
//             <div className="item-header">

//             </div>
//             <div className="content">
            
//             </div>

//           </article>
//         )

//     }

//   }
// }

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
                <a href={"http://"+ jobs[key].url}>
                  {jobs[key].company}
                </a>
              </span>
              <span className="title item-title">
                {jobs[key].position}
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
      <h1 className="section-header">My Toolbox</h1>
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
    <div className="resume">
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

// ======================================================================================= //
// ======================================================================================= //
// ==================================== Control Panel ==================================== //
// ======================================================================================= //
// ======================================================================================= //

// class CtrlPanelItem extends React.Component {
//   render() {
//     var text = this.props.text
//     var id = this.props.id
//     var lvl = this.props.lvl
//     return (
//       <div id={id} className={"lvl"+lvl}>
//         <input type="checkbox" name={id}></input>
//         <label for={id}>{text}</label>
//       </div>
//     )
//   }
// }


// class ControlPanel extends Component {
//   constructor() {
//     super();
//     this.htmlArr = []
//   }

//   iterate(obj, lvl, id){
//     var that = this
//     Object.keys(obj).forEach(function(key){

//       var child = obj[key]
//       var childLen = Object.keys(child).length

//       if (typeof child == "string") {
//         id = id+"-"+key
//         that.htmlArr.push(<CtrlPanelItem text={child} id={id} lvl={lvl} ></CtrlPanelItem>)
//       }
//       else if (childLen >= 0) {
//         id = id+"-"+key
//         var text = key.replace( /([A-Z])/g, " $1" );
//         text = text.charAt(0).toUpperCase() + text.slice(1);
//         that.htmlArr.push(<CtrlPanelItem text={text} id={id} lvl={lvl}></CtrlPanelItem>)
//         that.iterate(child, lvl+1, id)
//       }
//       return that.htmlArr
//     });

//     console.log(that.htmlArr)
//     return (that.htmlArr)
//   }

//   render() {

//     console.log(this.props)
//     return(
//       <div className="control-panel">
//         <header><h1>Control Panel</h1></header>

//         <form>
//           {

//             this.iterate(this.props, 0, "")

//             // foreach element in Object

//             //   if element is a string, 
//               // then add checkbox with string as label to html

//             //   else if element is not a string and is longer than 0
//             //     then add checkbox with name as label to html
//             //     and then iterate through element

//           }
//         </form>
//       </div>
//     )
//   };
// }


// ======================================================================================= //
// ======================================================================================= //
// ========================================= APP ========================================= //
// ======================================================================================= //
// ======================================================================================= //

class App extends Component {
  componentDidMount() {

  }

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