# LYRPD_site

A site for Love Your Rescue Pet Day for Austin Pets Alive.

Love Your Rescue Pet Day (LYRPD) has been a day where various businesses all over the city commit to donating 10% of their sales to APA!. While it has been a great fundraiser for us in the past, we wanted to make it more of an interactive fundraiser. 

This year, we would really like to bring in the focus to truly LOVE on your resuce pet - aka: spending time with them, picking up a special treat for them, etc. We'd like to bring a few businesses on to have "Pet Stops" - an activity that people can do with/for their pet. For example, decorate a bandana for their pet.

We'd love to have an interactive map that shows where all of the pet stops are, as well as participating businesses (those that are donating 10% of sales that day, but don't have the added activity.) Our current plan is to have the Pet Stops all in the same area of town (78704).

## How to run it

1. Install [Docker](http://docker.com) in your machine.

2. Clone this repository.

3.  Run:
    ```
    $ cd LYRPD_site
    <edit the file docker-compose.yml to add your keys>
    $ docker-compose build
    $ docker-compose up
    ```

# LICENSE

The "Love Your Rescue Pet Day" code is licensed under the terms of the GNU Affero General Public License.

Copyright © 2017 Shelby Haverda, William Gilmore, Walter Moreira

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see http://www.gnu.org/licenses/.