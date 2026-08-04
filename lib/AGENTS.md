# Shared-code instructions

`lib/` contains build pipelines and reusable utilities shared by multiple
questions. Keep shared code generic and data-driven; question-exclusive code
belongs under that question's `code/` directory.

Promote code here only after a second question genuinely needs it. When
promoting a pipeline or derived-data helper, document its current consumers
in a header comment, following `build_transmission_volume.sh`.
