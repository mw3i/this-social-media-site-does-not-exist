---
layout: root.html
title: Profiles
---
{% assign profiles = "SELECT * FROM profiles" | sql %}
<section class="section">
    <div class="container is-max-desktop">
        <div class="columns is-centered">
            <div class="column is-three-quarters">
                <div class="columns is-multiline">
                    {% for profile in profiles %}
                    <!-- Profile Card -->
                    <div class="column is-full">
                        <div class="card has-background-grey-darker" style='box-shadow: none;'>
                            <div class="card-content">
                                <div class="columns">
                                    <!-- Left Column with Name and Profile Picture -->
                                    <div class="column is-one-third">
                                        <h3 class="title is-4">{{ profile.name }}</h3>
                                        {% if profile.profile_pic_path %}
                                        <figure class="image is-128x128">
                                            <img class='is-rounded' src="/-/images/{{ profile.id }}.png" alt="{{ profile.name }}'s profile picture">
                                            <!-- <img src="{{ profile.profile_pic_path }}" alt="{{ profile.name }}'s profile picture"> -->
                                        </figure>
                                        {% else %}
                                        <figure class="image is-128x128">
                                            <img src="https://via.placeholder.com/128" alt="Placeholder image">
                                        </figure>
                                        {% endif %}
                                    </div>
                                    <!-- Right Column with Info, vertically centered -->
                                    <div class="column is-flex is-align-items-center">
                                        <div>
                                            <p><strong>Nationality:</strong> {{ profile.nationality }}</p>
                                            <p><strong>Political Ideology Leaning:</strong> {{ profile.political_ideology_leaning | round: 2 }}</p>
                                            <p><strong>Interests:</strong> {{ profile.interests | join: ", " }}</p>
                                            <!-- <p><strong>Mood:</strong> {{ profile.mood }}</p> -->
                                            <p><strong>Personality Type:</strong> {{ profile.personality_type }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</section>
