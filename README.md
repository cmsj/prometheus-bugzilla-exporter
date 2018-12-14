[![Build Status](https://dev.azure.com/cmsj/cmsj/_apis/build/status/cmsj.prometheus-bugzilla-exporter)](https://dev.azure.com/cmsj/cmsj/_build/latest?definitionId=2)

# Prometheus Bugzilla Exporter

## Introduction

The purpose of this project is to export basic data about Bugzilla search results, in a format that Prometheus can consume. Specifically, as text files that can be ingested by node-exporter's textfile collector.

## Requirements

 * You should have a directory somewhere that is being monitored by node-exporter's textfile collector
 * Python 3 (tested against 3.7)
 * The [simple_rest_client](https://pypi.org/project/simple-rest-client/) Python module
 * Bugzilla REST API (available from v5 of Bugzilla)

## Installation

You have three main options here:

### From Source

`pip install /path/to/this/repo`

### From pip

`pip install prombzex`

### Via Docker

`docker pull cmsj/prometheus-bugzilla-exporter`

Note that if you use the Docker image, there are two expected volumes to mount:

 * `/config.json` - The configuration file for prombzex (see Configuration below)
 * `/outdir` - A directory that the textfile outputs will be written to

### Configuration

Prombzex is configured via a JSON file, the path/name of which should be supplied as the only command line argument when running prombzex.

The file should look like this:

```json
{
    "default": {
        "timeout": 60,
        "output_dir": "/outdir"
    },
    "https://bugzilla.someproject.org": {
        "output_file": "someproject.prom",
        "name": "Some Project",
        "api_key": "12345678abcdef",
        "queries": [
            {
                "name": "my_open_bugs",
                "help": "Count of bugs I have open right now",
                "type": "gauge",
                "query": "https://bugzilla.someproject.org/buglist.cgi?bug_status=__open__&email1=MYEMAIL%40SOMEPROJECT.ORG&emailassigned_to1=1&emailtype1=substring&list_id=9810932&query_format=advanced"
            },
            {
                "name": "my_closed_all_time",
                "help": "Count of bugs I've ever closed",
                "type": "counter",
                "query": "https://bugzilla.someproject.org/buglist.cgi?bug_status=__closed__&email1=MYEMAIL%40SOMRPROJECT.ORG&emailassigned_to1=1&emailtype1=substring&list_id=9810932&query_format=advanced"
            }
        ]
    }
    "https://bugzilla.othergroup.net": {
        "output_file": "othergroup.prom",
        "name": "Other Group",
        "api_key": "abcdef1234568",
        "queries": [
            {
                "name": "some_query_name",
                "help": "Some interesting query",
                "type": "gauge",
                "group_field": "status",
                "params": [
                    { "key": "status", "value": "__open__" },
                    { "key": "f1", "value": "assigned_to" },
                    { "key": "o1", "value": "substring" },
                    { "key": "v1", "value": "helpfulcorp.com" },
                    { "key": "list_id", "value": "12345678" },
                    { "key": "query_format", "value": "advanced" },
                    { "key": "include_fields", "value": ["id", "status"] }
                ]
            }
        ]
    }
}
```

Obviously, some explanation is required here!

The structure is that there should be dictionaries for each Bugzilla server you want to talk to and optionally a `default` dictionary to provide default values that may be overidden in some of the server configs.

The keys available in each server are:

Note that the URL for the server is the key in the top-level dictionary. Hostnames specified in a `query` field are ignored, only the query parameters are parsed.

 * `name`: A friendly name for the Bugzilla server
 * `api_key`: The API key you obtain from your Bugzilla preferences
 * `queries`: An array of dictionaries, each of which defines a search query to run against the server (see below)
 * `timeout`: A number of seconds to wait before giving up on search queries. The underlying default in `simple_rest_client` is a few seconds and is likely to be much too short for even moderately complex Bugzilla queries. Strongly consider setting a high timeout in the `default` section of your `config.json`.
 * `output_dir`: The directory where output files should be written - in the case of Docker, to match the Dockerfile, you should set this in `default` to `/outdir`.
 * `output_file`: The filename to create in `output_dir` with the Prometheus values. There is no particular need for this to be specified per-server, but you may prefer that layout. Note that for the textfile collector to notice the file, it must end with `.prem`.

The keys available on queries are:

 * `name`: A Prometheus-compatible name to uniquely identify the query
 * `help`: A human-compatible description of the data the query represents
 * `type`: At the moment, only `gauge` and `counter` are supported - these are hints to Prometheus for whether the value can go up and down, or only up (respectively).
 * `group_field`: (optional) If present, this field will group the results by a given field in the output (it by a particular column in the Bugzilla results). Useful if you want to do things like separate graph lines for different bug states with `group_field` set to `status` (assuming the Status column is included in your result fields)
 * `query`: A complete Bugzilla URL, which you should generate using the normal Bugzilla advanced search interface.
 * `params`: A representation of all of the query parameters from a complete Bugzilla URL. This is easier to read than a complete Bugzilla URL, but harder to create and doesn't offer any strong benefits unless you will be editing the query a lot.
