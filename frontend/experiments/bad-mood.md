---
layout: root.html
title: Comments With Bad Mood
---

Mood intensity sampled with mean of 1; Personal mood set to: "really bad mood; very annoyed"

...it's hard to make chatgpt sound angry :/

<style type="text/css">
#tooltip {
    position: fixed;
    top: 40px;
    bottom: 40px;
    left: -35vw;
    padding: 30px;
    background-color: rgba(0, 0, 0, 0.85);
    color: white;
    border-radius: 14px;
    font-size: 0.875rem;
    z-index: 1000;
    width: 30vw;
    transition: transform 0.5s ease-in-out;
}

.tooltip-shown {
    transform: translateX(37vw);
}
</style>
<section class="section">
    <div class="container is-max-tablet">
        <h1 class="title">Feed</h1>
        {% assign posts = "SELECT posts.*, profiles.name AS profile_name FROM posts JOIN profiles ON posts.user = profiles.id" | sql %}
        {% for post in posts %}
        <div class="my-6 box content has-background-black-ter" style='box-shadow: none !important;'>
            <article class="media" data-prompt-tooltip={{ post.prompt | escape | jsonify }}>
                <figure class="media-left">
                    <p class="image is-64x64">
                        <!-- <img src="{{ post.user.profile_pic_path }}" alt="Profile Picture"> -->
                        <img class="is-rounded" src="/-/images/{{ post.user }}.png" alt="Profile Picture">
                    </p>
                </figure>
                <div class="media-content">
                    <div class="content">
                        <p>
                            <strong>{{ post.profile_name }}</strong> <small class="is-pulled-right has-text-grey-light">{{ post.date | date: '%B %d, %Y' }}</small>
                            <br>
                            {{ post['post-content'] }}
                            <!-- Make sure to use 'post_content' to display the text -->
                        </p>
                    </div>
                </div>
            </article>
            <div class="comments mt-4 p-4 has-background-grey-darker box" style="padding-left: 5rem !important; box-shadow: none;">
                <!-- Indentation for comments -->
                {% assign comments_query = "SELECT comments_bad_mood.*, profiles.id AS profile_id, profiles.name AS profile_name FROM comments_bad_mood JOIN profiles ON comments_bad_mood.user = profiles.id WHERE comments_bad_mood.post = " | append: post.id %}
                {% assign comments = comments_query | sql %}
                {% for comment in comments %}
                <article class="media mt-2">
                    <figure class="media-left">
                        <p class="image is-48x48">
                            <img class="is-rounded" src="/-/images/{{ comment.profile_id }}.png" alt="Profile Picture">
                        </p>
                    </figure>
                    <div class="media-content" data-prompt-tooltip={{ comment.prompt | escape | jsonify }}>
                        <div class="content">
                            <p>
                                <strong>{{ comment.profile_name }}</strong> (mood: {{ comment.mood | round: 2}}) <small class="has-text-grey-light is-pulled-right"></small>
                                <br>
                                {{ comment.comment_content }}
                            </p>
                        </div>
                    </div>
                </article>
                {% endfor %}
            </div>
        </div>
        <hr>
        {% endfor %}
    </div>
</section>
<div id='tooltip'>
</div>

<script type="text/javascript">
const tooltip = document.querySelector('#tooltip');
document.addEventListener('DOMContentLoaded', function() {
    // Select all elements with the data-prompt-tooltip attribute
    const tooltipElements = document.querySelectorAll('[data-prompt-tooltip]');

    tooltipElements.forEach(function(el) {

        // Show the tooltip on mouse enter
        el.addEventListener('mouseenter', function() {
            tooltip.innerHTML = `PROMPT: <br><br>${el.getAttribute('data-prompt-tooltip')}`; // Set tooltip text

            // Add the class to show the tooltip (slide-in effect)
            tooltip.classList.add('tooltip-shown');
        });

        // Hide the tooltip on mouse leave
        el.addEventListener('mouseleave', function() {
            tooltip.classList.remove('tooltip-shown'); // Remove the class to hide the tooltip
        });
    });
});
</script>