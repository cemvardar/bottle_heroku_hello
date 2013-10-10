    <select name="gazeteler" id="{{!row_collection_name}}">
        %for gazete in gazeteler:
            <option value="{{!gazete}}">{{!gazete}}</option>
        %end
    </select>