import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";
import { LANG } from "../constant";

const LanguageSelector = ({ value = LANG.ENGLISH.value, onChange }) => {
    return (
        <FormControl variant="standard" sx={{ m: 1, width: { xs: '100%', sm: '50%' } }}>
            <InputLabel id="language-selector-input-label">Language</InputLabel>
            <Select
                labelId="language-selector-label"
                id="language-selector"
                label="Language"
                value={value}
                defaultValue={LANG.ENGLISH.value}
                onChange={onChange}
            >
                {Object.keys(LANG).map((key) => (
                    <MenuItem value={LANG[key].value} >{LANG[key].label}</MenuItem>
                )
                )}
            </Select>
        </FormControl>
    );
}

export default LanguageSelector;