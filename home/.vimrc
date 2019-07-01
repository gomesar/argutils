filetype plugin indent on
" statusline
set laststatus=2
" Add file path
set statusline=%F%m%r%h%w\ [F:%{&ff},\ T:%Y]\ [ASCII:\%03.3b,\ HEX:\%02.2B]\ (%l,\ %v)[%03p%%-%L]
" set statusline+=%F

" show existing tab with 4 spaces width
set tabstop=4
" when indenting with '>', use 4 spaces width
set shiftwidth=4
" On pressing tab, insert 4 spaces
set expandtab

execute pathogen#infect()
call pathogen#helptags()
map <C-t> :NERDTreeToggle<CR>
" YAML stuff
autocmd FileType yaml setlocal ts=2 sts=2 sw=2 expandtab

" Enable indent-guide
colorscheme default
map <C-i> :IndentGuidesToggle<CR>
let g:indent_guides_auto_colors = 0
hi IndentGuidesOdd  ctermbg=red
hi IndentGuidesEven ctermbg=yellow
