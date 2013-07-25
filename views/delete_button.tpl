<form id = "{{data['form_id']}}" action="/koseyazisi/{{data['user_id']}}/sil" method="POST" style="display: inline;">
    <input name="object_id" id="object_id" type="hidden" value={{data['object_id']}} />
    <input name="url" id="url" type="hidden" value="{{data['url']}}" />
    <input type="submit" class="deleteButton" value="Sil"/>
</form>