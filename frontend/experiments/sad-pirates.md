---
layout: root.html
title: Commenters are Sad Pirates
---

Prompt appended with: "ALSO: make sure you talk like a really sad pirate the whole time"

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
                        <img class="is-rounded" src="{{ baseUrl }}/-/images/{{ post.user }}.png" alt="Profile Picture">
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
                {% assign comments_query = "SELECT comments_sad_pirates.*, profiles.id AS profile_id, profiles.name AS profile_name FROM comments_sad_pirates JOIN profiles ON comments_sad_pirates.user = profiles.id WHERE comments_sad_pirates.post = " | append: post.id %}
                {% assign comments = comments_query | sql %}
                {% for comment in comments %}
                <article class="media mt-2">
                    <figure class="media-left">
                        <p class="image is-48x48">
                            <img class="is-rounded" src="{{ baseUrl }}/-/images/{{ comment.profile_id }}.png" alt="Profile Picture">
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

        el.addEventListener('click', function(event) {
            // Prevent click from bubbling up if the element is clicked
            event.stopPropagation();

            // Check if tooltip is already shown
            if (tooltip.classList.contains('tooltip-shown')) {
                // Hide the tooltip if it is already visible
                tooltip.classList.remove('tooltip-shown');
            } else {
                // Set tooltip content and show it
                tooltip.innerHTML = `PROMPT: <br><br>${el.getAttribute('data-prompt-tooltip')}`;
                tooltip.classList.add('tooltip-shown');
            }
        });

        // // Show the tooltip on mouse enter
        // el.addEventListener('mouseenter', function() {
        //     tooltip.innerHTML = `PROMPT: <br><br>${el.getAttribute('data-prompt-tooltip')}`; // Set tooltip text

        //     // Add the class to show the tooltip (slide-in effect)
        //     tooltip.classList.add('tooltip-shown');
        // });

        // // Hide the tooltip on mouse leave
        // el.addEventListener('mouseleave', function() {
        //     tooltip.classList.remove('tooltip-shown'); // Remove the class to hide the tooltip
        // });
    });
});
</script>