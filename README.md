# Project: Logs Analysis
## Project I: FSWD Udacity

## Introduction
This is a project that is part of the Full Stack Web Developer Nanodegree ([FSWD](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)) by [Udacity](www.udacity.com) in partnership with [Google](https://google.com), [AWS](https://aws.amazon.com), [Github](https://github.com), and [AT&T](https://www.att.com).  
This project is for stretching the SQL database skills, by getting practice interacting with a live database both from the command line and form the code.  The database that has been used contains millions of rows, and I should build and refine complex queries and use them to draw business conclusions from data.

### Report Generation
Report generation
Building an informative summary from logs is a real task that comes up very often in software engineering. For instance, at Udacity we collect logs to help us measure student progress and the success of our courses. The reporting tools we use to analyze those logs involve hundreds of lines of SQL 

### Database as shared resource
In this project, you'll work with data that could have come from a real-world web application, with fields representing information that a web server would record, such as HTTP status codes and URL paths. The web server and the reporting tool both connect to the same database, allowing information to flow from the web server into the report.

This shows one of the valuable roles of a database server in a real-world application: it's a point where different pieces of software (a web app and a reporting tool, for instance) can share data.


## Installation
To start on this project, you'll need database software (provided by a Linux virtual machine) and the data to analyze.

### Prerequisites
You need to install psycopg2 to run the code.

`$ pip install psycopg2`

### The virtual machine
This project makes use a Linux-based virtual machine (VM), and we used tools called [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) to install and manage the VM.

### Install VirtualBox
VirtualBox is the software that actually runs the virtual machine. You can download it from [virtualbox.org](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Currently (October 2017), the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.

**Ubuntu users**: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

### Install Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from vagrantup.com. Install the version for your operating system.

**Windows users**: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

### Download the VM configuration
There are a couple of different ways you can download the VM configuration.

You can download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) This will give you a directory called **FSND-Virtual-Machine**. It may be located inside your **Downloads** folder.

**Note**: If you are using Windows OS you will find a Time Out error, to fix it use the new [Vagrant file configuration](https://s3.amazonaws.com/video.udacity-data.com/topher/2019/March/5c7ebe7a_vagrant-configuration-windows/vagrant-configuration-windows.zip) to replace you current Vagrant file.

Alternately, you can use Github to fork and clone the repository [https://github.com/udacity/fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm).

Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory

### Start the virtual machine
From your terminal, inside the vagrant subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!

### Download the data
Next, [download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called `newsdata.sql`. Put this file into the `vagrant` directory, which is shared with your virtual machine.

To build the reporting tool, you'll need to load the site's data into your local database.

To load the data, `cd` into the `vagrant` directory and use the command `psql -d news -f newsdata.sql`
Here's what this command does:

`psql` — the PostgreSQL command line program
`-d news` — connect to the database named news which has been set up for you
`-f newsdata.sql` — run the SQL statements in the file newsdata.sql
Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

> This will give you the PostgreSQL database and support software needed for this project. If you have used an older version of this VM, you may need to install it into a new directory.

> If you need to bring the virtual machine back online (with vagrant up), do so now. Then log into it with vagrant ssh.

## Database
The database contains three tables, and the `psql` command to see all tables is `\dt`:   

| Schema | Name     | Type  | Owner   |
|:---    |:---      |:---   |:---     |
| public | articles | table | vagrant |
| public | authors  | table | vagrant |
| public | log      | table | vagrant |

A description of each table:    

| Table        | Description                                                                           |
|:---          |:---                                                                                  |
| **articles** | stores article information such as the author and title                              |
| **authors**  | stores information about the authors such as their name and their author id          |
| **logs**     | sotres information on when articles were accessed, such as date and request response |

The `psql` command to see each table structure is `\d`.
 
## articles Table
`\d articles`   

| column | Type                     | Modifiers                                             |
|:---    |:---                      |:---                                                   |
| author | integer                  | not null                                              |
| title  | text                     | not null                                              |
| slug   | text                     | not null                                              | 
| lead   | text                     |                                                       |
| body   | text                     |                                                       | 
| time   | timestamp with time zone | default now()                                         |
| id     | integer                  | not null default nextval('articles_id_seq'::regclass) |

**Indexes**:
    "articles_pkey" PRIMARY KEY, btree (id)
    "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)

**Foreign-key constraints**:
    "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

## authors Table
`\d authors`

| Column |  Type   | Modifiers                                            |     
|:---    |:---     |:---                                                  |
| name   | text    | not null                                             |
| bio    | text    |                                                      |
| id     | integer | not null default nextval('authors_id_seq'::regclass) |

**Indexes**:
    "authors_pkey" PRIMARY KEY, btree (id)

**Referenced by**:
    TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

## log Table
`\d log`

| Column | Type                     | Modifiers                                        |                     
|:---    |:---                      |:---                                              |
| path   | text                     |                                                  |
| ip     | inet                     |                                                  |
| method | text                     |                                                  |
| status | text                     |                                                  |
| time   | timestamp with time zone | default now()                                    |
| id     | integer                  | not null default nextval('log_id_seq'::regclass) |

**Indexes**:
    "log_pkey" PRIMARY KEY, btree (id)

> The database that you're working with in this project is running `PostgreSQL`

## Usage
### Running the Program
Download the file `log_main.py` into the `vagrant` folder, and run the application with the following command:
`python3 log_main.py`.

You can compare the results with the data contained in the `outputExample.txt` file.  The data should be the same.

### Questions to Solve
1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.
2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.
3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)

## Authors
[**Oscar Reyes**](https://github.com/or73)

## License
This project is licensed under MIT license

## Acknowledgements
* Thanks to [Udacity](https://udacity.com)
